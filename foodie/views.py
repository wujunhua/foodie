from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserChangeForm
from carton.cart import Cart
from .models import Menu, UserProfile, Order, OrderItem, Feedback
from .forms import CreateUserForm, AddressForm, FeedbackForm, EditProfileForm, CreateEmployeeForm

def index(request):
    context = {
            'menu_favorites':  Menu.objects.order_by('-rating')[:5]
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == 'GET':
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})
    elif request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login') #Redirect to customer page in future
        return render(request, 'register.html', {'form': form})

def register_employee(request):
    if request.method == 'GET':
        form = CreateEmployeeForm()
        return render(request, 'register_employee.html', {'form': form})
    elif request.method == 'POST':
        form = CreateEmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/login')
        return render(request, 'register_employee.html', {'form': form})

@login_required(login_url='/login/')
def menu(request):
    menu = Menu.objects.filter(on_menu=True)
    menu = [menu[x:x+4] for x in range(0, len(menu), 4)]
    user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
    return render(request, 'menu.html', {'menu': menu, 'certified': user_profile.certified})

def add(request):
    cart = Cart(request.session)
    item = Menu.objects.get(pk=request.GET.get('menu_id'))

    if request.user.groups.filter(name="vip").exists():
        cart.add(item,price=item.vip_price)
    else:
        cart.add(item, price=item.price)

    message = 'Added ' + item.name + ' to cart'
    messages.success(request, message)
    return HttpResponseRedirect('/menu')

def remove(request):
    cart = Cart(request.session)
    item = Menu.objects.get(pk=request.GET.get('menu_id'))
    cart.remove(item)
    return HttpResponseRedirect(request.GET.get('next'))

def checkout(request):
    user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
    if request.method == 'GET':
        cart = Cart(request.session)
        form = AddressForm()
        return render(request, 'checkout.html', {'form': form, "nav_on":True, "cart": cart, 'money': user_profile.money})
    elif request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            cart = Cart(request.session)

            order = Order.objects.create(
                        customer_id=user_profile.id,
                        address=form.cleaned_data['address'],
                        total = cart.total,
                        frozen = user_profile.money < cart.total
                    )
            for item in cart.items:
                order_item = OrderItem.objects.create(order=order,
                                                      item=item.product,
                                                      quantity=item.quantity,
                                                      subtotal=item.subtotal )
            if not order.frozen:
                user_profile.update(cart.total)
                user_profile.save()
            cart.clear()
            return render(request, 'order_success.html', {'address': order.address,'order_no': order.id, 'frozen': order.frozen, 'nav_on': True})

def orders(request):
    user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
    orders = Order.objects.filter(customer_id=user_profile.id)
    print(orders)
    return render(request, 'orders.html', {'nav_on': True, 'orders': orders})

def rate_food(request):
    order_item = OrderItem.objects.filter(id=request.POST.get('id')).first()
    order_item.food_rating = float(request.POST.get("rating"))
    order_item.save()
    return HttpResponse('')

def rate_delivery(request):
    order_item = OrderItem.objects.filter(id=request.POST.get('id')).first()
    order_item.delivery_rating = float(request.POST.get("rating"))
    order_item.save()
    return HttpResponse('')

def feedback(request):
    if request.method == 'GET':
        form = FeedbackForm(feedback_type=request.GET.get('type'), order_item_id=request.GET.get('order_item_id'))
        return render(request, 'feedback.html', {'form': form, 'type': request.GET.get('type'),'nav_on': True})
    elif request.method == 'POST':
        print(request.GET.get('type'))
        form = FeedbackForm(request.GET.get('type'), request.GET.get('order_item_id'), request.POST)
        if form.is_valid():
            employee = None
            if request.POST.get('employee') == FeedbackForm.CHEF:
                employee = OrderItem.objects.filter(id=request.GET.get('order_item_id')).first().item.created_by
            else:
                employee = OrderItem.objects.filter(id=request.GET.get('order_item_id')).first().order.delivered_by

            user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
            feedback_model = Feedback.objects.create(customer=user_profile,
                                                     feedback=form.cleaned_data['feedback'],
                                                     employee=employee
                    )
            if request.GET.get('type') == 'compliment':
                feedback_model.feedback_type = Feedback.CMPLAINT
            else:
                feedback_model.feedback_type = Feedback.CMPMENT
            feedback_model.save()
            return HttpResponseRedirect(reverse('orders'))

def profile(request):
    args = {'user':request.user}
    return render(request, 'profiles.html',args)

def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return redirect('/')

    else:
        form = EditProfileForm(instance = request.user)
        args = {'form':form}
        return render(request, 'edit_profile.html', args)

def feedbacks(request):
    feedbacks = Feedback.objects.filter(manager_seen=False)
    return render(request, 'complaint.html', {'feedbacks': feedbacks, 'nav_on': True})

def valid(request):
    feedback = Feedback.objects.filter(id=request.GET.get('id')).first()
    if feedback.feedback_type == Feedback.CMPMENT:
        feedback.employee.got_compliment()
    else:
        feedback.employee.got_complaint()
    feedback.employee.save()
    feedback.manager_seen = True
    feedback.save()
    return HttpResponseRedirect(reverse('feedbacks'))

def invalid(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    feedback = Feedback.objects.filter(id=request.GET.get('id')).first()
    user_profile.warn()
    user_profile.save()

    feedback.manager_seen = True
    feedback.save()
    return HttpResponseRedirect(reverse('feedbacks'))
