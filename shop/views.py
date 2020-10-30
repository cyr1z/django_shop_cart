from datetime import datetime, timedelta
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.safestring import mark_safe
from django.views.generic import DetailView, ListView, CreateView, \
    UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView

from shop.forms import SignUpForm, ProductCreateForm, PurchaseCreateForm, \
    ReturnCreateForm
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'form': ReturnCreateForm})
        return context


class ReturnListView(ListView):
    model = Return
    paginate_by = 10
    template_name = 'return_list.html'
    queryset = Return.objects.all()


class PurchaseCreate(CreateView):
    """
    Create a purchase
    """
    form_class = PurchaseCreateForm
    model = Purchase
    success_url = '/'

    def form_valid(self, form):
        # change redirect url
        self.success_url = f"/purchases/{self.request.user.id}"
        # save form data to object, not to database
        purchase = form.save(commit=False)
        # add  a selected product to object purchase
        product_id = self.request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        purchase.product = product
        # add current user to object purchase
        purchase.user = self.request.user
        # Check if enough money and products
        if purchase.count <= purchase.product.count:
            if purchase.user.purse >= purchase.cost_in_cents:
                # move money and product counts
                purchase.user.purse -= purchase.cost_in_cents
                purchase.product.count -= purchase.count
                # saving changed objects
                purchase.user.save()
                purchase.product.save()
                purchase.save()
            else:
                # Not enough money
                pass
        else:
            # Not enough product
            pass

        return super().form_valid(form=form)


class ReturnCreate(CreateView):
    form_class = ReturnCreateForm
    model = Return
    success_url = '/'

    def form_valid(self, form):
        # change redirect url
        self.success_url = f"/purchases/{self.request.user.id}"
        # save form data to object, not to database
        purchase_return = form.save(commit=False)
        # get the purchase object
        purchase_id = self.request.POST.get('purchase_id')
        purchase = Purchase.objects.get(id=purchase_id)
        # add the purchase to return object
        purchase_return.purchase = purchase
        # check purchase time not older of 3 minutes
        purchase_time = purchase_return.purchase.created_at
        now = timezone.now()
        if now < purchase_time + timedelta(minutes=3):
            # save object
            purchase_return.save()
            return super().form_valid(form=form)
        else:
            # Purchase too old. No return possible.
            pass


class ReturnApprove(DeleteView):
    model = Return
    success_url = '/returns/'

    def delete(self, request, *args, **kwargs):
        """
        Call the delete() method on the fetched object and then redirect to the
        success URL.
        """
        purchase_return = self.get_object()
        purchase = purchase_return.purchase
        user = purchase.user
        user.purse += purchase.cost_in_cents
        product = purchase.product
        product.count += purchase.count
        user.save()
        product.save()
        purchase.delete()
        purchase_return.delete()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')


class ReturnCancel(DeleteView):
    model = Return
    template_name = 'base.html'
    success_url = '/returns/'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_superuser:
            return self.delete(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/')
