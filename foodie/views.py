from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from carton.cart import Cart
from .models import Menu, UserProfile, Order
from .forms import CreateUserForm, AddressForm

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
        print(form.errors)
        return render(request, 'register.html', {'form': form})

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
        cart.add(item,price=item.price * .9)
    else:
        cart.add(item, price=item.price)

    message = 'Added ' + item.name + ' to cart'
    messages.success(request, message)
    return HttpResponseRedirect('/menu')

def remove(request):
    cart = Cart(request.session)
    item = Menu.objects.get(pk=request.GET.get('menu_id'))
    cart.remove(item)
    return HttpResponseRedirect('/menu')

def checkout(request):
    if request.method == 'GET':
        cart = Cart(request.session)
        form = AddressForm()
        return render(request, 'checkout.html', {'form': form, "nav_on":True, "cart": cart})
    elif request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
            cart = Cart(request.session)

            order = Order.objects.create(
                        customer_id=user_profile.id,
                        address=form.cleaned_data['address'],
                        total = cart.total,
                        frozen = user_profile.money < cart.total
                    )
            for product in cart.products:
                order.items_ordered.add(product)
            order.save()
            cart.clear()
            user_profile.num_orders += 1
            user_profile.money_spent += cart.total
            user_profile.money -= cart.total
            user_profile.save()
            return render(request, 'order_success.html', {'order_no': order.id, 'nav_on': True})

