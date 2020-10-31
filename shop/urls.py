from django.urls import path

from shop.views import ProductListView, PurchaseListView, ReturnCreate, \
    ReturnListView, UserLogin, UserLogout, ProductCreate, PurchaseCreate, \
    ProductUpdate, Register, ReturnApprove, ReturnCancel

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('returns/', ReturnListView.as_view(), name='returns'),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('create/', ProductCreate.as_view(), name="create"),
    path('buy/', PurchaseCreate.as_view(), name='buy'),
    path('return/', ReturnCreate.as_view(), name='return'),
    path('edit/<int:pk>/', ProductUpdate.as_view(), name='edit'),
    path('approve/<int:pk>/', ReturnApprove.as_view(), name='approve'),
    path('cancel/<int:pk>/', ReturnCancel.as_view(), name='cancel'),
]
