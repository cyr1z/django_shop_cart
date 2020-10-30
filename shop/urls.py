from django.urls import path

from shop.views import ProductDetailView, ProductListView, PurchaseListView, \
    ReturnListView, UserLogin, UserLogout, Register, ProductCreate, \
    PurchaseCreate, ProductUpdate, ReturnApprove, ReturnCancel, ReturnCreate

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product'),
    path('purchases/', PurchaseListView.as_view(), name='purchases'),
    path('purchases/<int:user_id>/', PurchaseListView.as_view(),
         name='purchases'),
    path('returns/', ReturnListView.as_view(), name='returns'),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', UserLogout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('product_create/', ProductCreate.as_view(), name="product_create"),
    path('buy/', PurchaseCreate.as_view(), name='buy'),
    path('return/', ReturnCreate.as_view(), name='return'),
    path('product_edit/<int:pk>/', ProductUpdate.as_view(),
         name='product_edit'),
    path('return_approve/<int:pk>/', ReturnApprove.as_view(),
         name='return_approve'),
    path('return_cancel/<int:pk>/', ReturnCancel.as_view(),
         name='return_cancel'),
]
