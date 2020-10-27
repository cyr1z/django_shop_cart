# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import ShopUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = ShopUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = ShopUser
        fields = ('username', 'email')
