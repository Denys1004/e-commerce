from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(
      attrs={
        'class': 'form-control my-2',
        'placeholder': 'Enter your password',
         }))

    password2 = forms.CharField(widget=forms.PasswordInput(
      attrs={
        'class': 'form-control',
        'placeholder': 'Re enter your password'}))

    class Meta:
      model = User
      fields = ['username', 'email', 'password1', 'password2']

      widgets = {
      'username': forms.TextInput(attrs={'class': 'form-control my-2' , 'placeholder': 'Enter Username'}),
      'email': forms.EmailInput(attrs={'class': 'form-control' , 'placeholder': 'Enter Email Address'}),
      'password': forms.PasswordInput(attrs={'class': 'form-control'})
      }