from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from shop.forms import SignUpForm, ProductCreateForm, PurchaseCreateForm
from shop.models import Product, Purchase, Return


class UserLogin(LoginView):
    template_name = 'login.html'


class Register(CreateView):
    form_class = SignUpForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'form': PurchaseCreateForm})
        return context


class ProductCreate(CreateView):
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductCreateForm
    success_url = '/'


class ProductUpdate(UpdateView):
    model = Product
    template_name = 'product_edit.html'
    success_url = '/'
    fields = ['image', 'title', 'description', 'price', 'count']

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        img_url = self.object.image.url
        img_string = mark_safe(f'<img src="{img_url}" height="200">')
        context.update({'preview': img_string})
        return context


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


class PurchaseCreate(CreateView):
    form_class = PurchaseCreateForm
    model = Purchase
    success_url = '/'

    def form_valid(self, form):
        purchase = form.save(commit=False)
        product = Product.objects.get(id=self.request.POST.get('product_id'))
        purchase.product = product
        purchase.user = self.request.user
        self.success_url = f"/purchases/{self.request.user.id}"
        purchase.save()
        return super().form_valid(form=form)
