from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User, Group
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from crispy_forms.bootstrap import StrictButton
from django import forms
from .models import UserProfile

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Username','type' : 'text'}))
    password = forms.CharField(label="Password", max_length=30,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder' : 'Password','type' : 'password'}))

class CreateUserForm(UserCreationForm):
    username = forms.CharField(label="Username", max_length=30,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username','type' : 'text'}))
    password1 = forms.CharField(label="Password",
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'type': 'password'}))
    password2 = forms.CharField(label="Password confirmation",
            widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password Confirmation', 'type': 'password'}))
    first_name = forms.CharField(label="First Name", max_length=30,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name', 'type': 'text'}))
    last_name = forms.CharField(label="Last Name", max_length=30,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name', 'type': 'text'}))
    money = forms.IntegerField(label="Money",
            widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Money', 'type': 'text'}))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(CreateUserForm, self).save(commit=True)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user_profile = UserProfile()
        user_profile.user = user
        user_profile.money = self.cleaned_data['money']
        group, created = Group.objects.get_or_create(name='customer')
        user.groups.add(group)
        user.save()
        user_profile.save()
        return  user_profile

class AddressForm(forms.Form):
    address = forms.CharField(required=True,max_length=100)

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action= reverse('checkout')
        self.helper.layout = Layout(
                'address',
                StrictButton('Submit', type='submit', css_class='btn-secondary'),
                )
