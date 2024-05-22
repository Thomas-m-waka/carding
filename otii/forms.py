from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)
    phone_number = PhoneNumberField()

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']


    
    
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


