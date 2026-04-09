from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Введіть Email' ,
        required=True ,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ведіть Email',
        }))

    username = forms.CharField(
        label='Створіть псевдонім' ,
        required=True ,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Створіть Username' ,
        }))

    password1 = forms.CharField(
        label='Створіть пароль' ,
        required=True ,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Створіть Password' ,
        }))

    password2 = forms.CharField(
        label='Повторіть пароль' ,
        required=True ,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть Password' ,
        }))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
