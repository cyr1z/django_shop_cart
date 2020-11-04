from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.generic import ListView, CreateView, \
    UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView

from shop.forms import SignUpForm, ProductCreateForm, PurchaseCreateForm, \
    ReturnCreateForm
from shop.models import Product, Purchase, Return
from shop.decorators import super_user_required


class UserLogin(LoginView):
    """ login """
    template_name = 'login.html'


class Register(CreateView):
    """ Sign UP """
    form_class = SignUpForm
    success_url = "/login/"
    template_name = "register.html"


class UserLogout(LoginRequiredMixin, LogoutView):
    """ Logout """
    next_page = '/'
    redirect_field_name = 'next'


class ProductListView(ListView):
    """
    List of products
    """
    model = Product
    paginate_by = 10
    template_name = 'product_list.html'
    queryset = Product.objects.all()

    # Add form with "count" input and "Buy" button to list items
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context.update({'form': PurchaseCreateForm})
        return context


@method_decorator(super_user_required, name='dispatch')
class ProductCreate(LoginRequiredMixin, CreateView):
    """
    Create products. Only for administrators.
    """
    model = Product
    template_name = 'product_edit.html'
    form_class = ProductCreateForm
    success_url = '/'


@method_decorator(super_user_required, name='dispatch')
class ProductUpdate(LoginRequiredMixin, UpdateView):
    """
    Update products. Only for administrators.
    """
    model = Product
    template_name = 'product_edit.html'
    success_url = '/'
    fields = ['image', 'title', 'description', 'price', 'count']

    # add product image preview to context
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        img_url = self.object.image.url
        img_alt = self.object.title
        img_string = f'<img src="{img_url}" alt="{img_alt}" height="200">'
        context.update({'preview': mark_safe(img_string)})
        return context


@method_decorator(login_required, name='dispatch')
class PurchaseListView(LoginRequiredMixin, ListView):
    """
    List of user purchases
    """
    model = Purchase
    paginate_by = 10
    template_name = 'purchase_list.html'

    # add user filter to queryset
    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


@method_decorator(super_user_required, name='dispatch')
class ReturnListView(LoginRequiredMixin, ListView):
    """
    Returns list. Only for administrators.
    """
    model = Return
    paginate_by = 10
    template_name = 'return_list.html'
    queryset = Return.objects.all()


@method_decorator(login_required, name='dispatch')
class PurchaseCreate(LoginRequiredMixin, CreateView):
    """
    Create a purchase
    """
    form_class = PurchaseCreateForm
    model = Purchase
    success_url = '/purchases/'

    def form_valid(self, form):
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
                messages.error(self.request, 'Not enough money.')
                return HttpResponseRedirect('/')
        else:
            # Not enough product
            messages.error(self.request, f'Not enough product. We have only'
                                         f' {purchase.product.count} on stock')
            return HttpResponseRedirect("/")

        return super().form_valid(form=form)


@method_decorator(login_required, name='dispatch')
class ReturnCreate(LoginRequiredMixin, CreateView):
    """
    Create return
    """
    form_class = ReturnCreateForm
    model = Return
    success_url = '/purchases/'

    def form_valid(self, form):
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
            messages.success(self.request, 'Purchase return request sent.')
            return super().form_valid(form=form)
        else:
            # Purchase too old. No return possible.
            messages.error(self.request,
                           'Purchase too old. No return possible.')
            return HttpResponseRedirect(self.success_url)


@method_decorator(super_user_required, name='dispatch')
class ReturnApprove(LoginRequiredMixin, DeleteView):
    """
    Admin approve return
    """
    model = Return
    success_url = '/returns/'


@method_decorator(super_user_required, name='dispatch')
class ReturnManage(LoginRequiredMixin, DeleteView):
    """
    Admin approve or reject =return
    """
    model = Return
    success_url = '/returns/'

    def delete(self, request, *args, **kwargs):
        purchase_return = self.get_object()
        if self.request.POST['act'] == 'approve':
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
