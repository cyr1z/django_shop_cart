from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from shop.models import ShopUser, Product, Purchase


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    last_name = forms.CharField(
        max_length=30, required=False,
        help_text='Optional.')
    email = forms.EmailField(
        max_length=254,
        help_text='Required. Inform a valid email address.')

    class Meta:
        model = ShopUser
        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2',)


class ProductCreateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'description', 'image', 'price', 'count']


class PurchaseCreateForm(ModelForm):
    count = forms.IntegerField(label='', initial='1')

    class Meta:
        model = Purchase
        fields = ['count', ]
