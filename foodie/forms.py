from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field
from crispy_forms.bootstrap import StrictButton, InlineRadios, InlineCheckboxes
from django import forms
from .models import UserProfile
from main.models import Employee

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
    address = forms.CharField(required=True,max_length=100,widget=forms.TextInput(attrs={'placeholder': 'address'}))

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action= reverse('checkout')
        self.helper.layout = Layout(
                'address',
                StrictButton('Submit', type='submit', css_class='btn-secondary'),
                )

class FeedbackForm(forms.Form):
    CHEF = "chef"
    DELIVERY = "delivery"
    EMPLOYEE_CHOICES = (
            (CHEF, "Chef"),
            (DELIVERY, "Delivery"),
            )

    employee = forms.ChoiceField(choices=EMPLOYEE_CHOICES)
    feedback = forms.CharField(required=True, widget=forms.Textarea())

    def __init__(self, feedback_type, order_item_id, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_action= reverse('feedback') + '?type=' + feedback_type + '&order_item_id=' + order_item_id
        self.helper.form_show_labels= False
        self.fields['employee'].label = False
        self.helper.layout = Layout(
                Field('feedback', rows="5", css_class='input-xlg'),
                Div(InlineRadios('employee'),
                    StrictButton('Submit', type='submit',
                        css_class='btn-secondary feedback-submit'), css_class="col-md-2"))

class EditProfileForm(UserChangeForm):
    first_name = forms.CharField(label="First Name", max_length=30,
            widget=forms.TextInput(attrs={'type': 'text', 'class':'form-control'}))
    last_name = forms.CharField(label="Last Name", max_length=30,
            widget=forms.TextInput(attrs={'type': 'text', 'class':'form-control'}))
    add_money = forms.IntegerField(label="Add Money",
            widget=forms.TextInput(attrs={'type': 'text', 'class':'form-control'}))

    class Meta:
        model = User
        fields = {
                'first_name',
                'last_name',
                'password'
        }

class CreateEmployeeForm(UserCreationForm):
    CHEF = "CH"
    DRVR = "DD"
    MNGR = "MG"

    POSITION_CHOICES = ((CHEF, 'Chef'), (DRVR, 'Delivery Driver'), (MNGR, 'Manager'))
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
    position =  forms.ChoiceField(choices=(POSITION_CHOICES), widget=forms.RadioSelect(attrs={'style':'margin:5px;'}))

    def save(self, commit=True):
        if not commit:
            raise NotImplementedError("Can't create User and UserProfile without database save")
        user = super(CreateEmployeeForm, self).save(commit=True)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        employee = Employee()
        employee.user = user

        position = self.cleaned_data['position']
        group = None
        permissions = Permission.objects.all()
        if position == self.CHEF:
            group, created = Group.objects.get_or_create(name='chef')
            permissions = permissions.filter(codename__contains='menu')
            for p in permissions:
                group.permissions.add(p)
            group.save()
        elif position == self.DRVR:
            group, created = Group.objects.get_or_create(name='driver')
        elif position == self.MNGR:
            group, created = Group.objects.get_or_create(name='manager')
            for p in permissions:
                group.permissions.add(p)
            group.save()

        user.groups.add(group)
        user.is_staff = True
        user.save()
        employee.save()
        return employee
