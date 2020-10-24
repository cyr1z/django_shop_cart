from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class ShopUser(AbstractUser):
    """
    Customised Django User Model
    Add purse - users money in "cents"/ Positive Integer
    unique combinations of First Name and Last Name
    """
    purse = models.PositiveIntegerField(
        default=1000000
    )

    class Meta:
        ordering = ["first_name", "last_name"]
        unique_together = ["first_name", "last_name"]
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return f'{self.get_username()} / {self.get_full_name()}'


class Product(models.Model):
    """
    Products
    """
    title = models.CharField(
        max_length=120
    )
    description = models.TextField(
        max_length=10000,
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='products_images',
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(
        default=0
    )
    stock_count = models.PositiveIntegerField(
        default=0
    )

#     Category = models.ManyToManyField(
#         Category,
#         null=True,
#         related_name='products'
#     )
#
#
# class Category(models.Model):
#     """
#     Category
#     """
#     title = models.CharField(
#         max_length=120
#     )


class Purchase(models.Model):
    """
    Purchase
    """
    user = models.ForeignKey(
        ShopUser,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_purchases'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        null=True,
        related_name='product_purchases'
    )
    count = models.PositiveIntegerField(
        default=0
    )
    created_at = models.DateField(
        default=timezone.now
    )


class Return(models.Model):
    """
    Return
    """
    purchase = models.ForeignKey(
        Purchase,
        on_delete=models.CASCADE,
        related_name='returns'
    )
    created_at = models.DateField(
        default=timezone.now
    )
