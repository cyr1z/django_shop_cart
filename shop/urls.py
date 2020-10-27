from django.contrib.auth.forms import UserCreationForm
from django.urls import path

from shop.views import ProductDetailView, ProductListView, PurchaseListView, \
    ReturnListView, UserLogin, UserLogout, Register

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('purchases/<int:user_id>/', PurchaseListView.as_view(),
         name='purchases'),
    path('returns/', ReturnListView.as_view(), name='returns'),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
]
