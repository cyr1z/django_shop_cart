# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView, FormView
from django.contrib.auth.views import LoginView, LogoutView

from shop.models import Product, Purchase, Return
from django.contrib.auth import get_user_model

User = get_user_model()


class UserLogin(LoginView):
    template_name = 'login.html'


class Register(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(Register, self).form_valid(form)


class UserLogout(LogoutView):
    next_page = '/'
    redirect_field_name = 'next'


class ProductDetailView(DetailView):
    model = Product


class ProductListView(ListView):
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'
    queryset = Product.objects.all()


class PurchaseListView(ListView):
    model = Purchase
    paginate_by = 10
    template_name = 'purchase_list.html'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class ReturnListView(ListView):
    model = Return
    paginate_by = 10
    template_name = 'return_list.html'
    queryset = Return.objects.all()
