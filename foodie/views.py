from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Menu
from .forms import CreateUserForm

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

def menu(request):
    menu = Menu.objects.all()
    menu = [menu[x:x+4] for x in range(0, len(menu), 4)]
    print(menu)
    return render(request, 'menu.html', {'menu': menu})
