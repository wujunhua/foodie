from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import views as auth_view
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from carton.cart import Cart
from .models import Menu, UserProfile
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
    menu = Menu.objects.all()
    menu = [menu[x:x+4] for x in range(0, len(menu), 4)]
    user_profile = UserProfile.objects.filter(user__id=request.user.id).first()
    print(user_profile)
    return render(request, 'menu.html', {'menu': menu, 'certified': user_profile.certified})

def add(request):
    cart = Cart(request.session)
    item = Menu.objects.get(pk=request.GET.get('menu_id'))
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
    form = AddressForm()
    return render(request, 'checkout.html', {'form': form, "nav_on":True})
