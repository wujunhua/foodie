"""food URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from . import views
from django.contrib.auth.decorators import user_passes_test


login_forbidden =  user_passes_test(lambda u: u.is_anonymous(), '/')

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', login_forbidden(auth_views.login),  {'template_name': 'login.html', 'authentication_form': LoginForm, 'extra_context':{'next' : '/'}}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^menu/$', views.menu, name='menu'),
    url(r'^add/$', views.add, name='add'),
    url(r'^remove/$', views.remove, name='remove'),
    url(r'^checkout/$', views.checkout, name='checkout'),
#   url(r'^', include('main.urls')),
    url(r'^admin/', admin.site.urls),
]
