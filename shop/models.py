from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.safestring import mark_safe


class ShopUser(AbstractUser):
    """
    Customised Django User Model
    Add purse - users money in "cents"/ Positive Integer
    unique combinations of First Name and Last Name
    """
    purse = models.PositiveIntegerField(
        default=1000000
    )

    @property
    def real_purse(self):
        return '$' + "{:.2f}".format(self.purse / 100)

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
        upload_to='static/products_images',
        null=True,
        blank=True
    )
    price = models.PositiveIntegerField(
        default=0
    )
    count = models.PositiveIntegerField(
        default=0
    )

    @property
    def real_price(self):
        return '$' + "{:.2f}".format(self.price / 100)

    @property
    def preview(self):
        img_url = self.image.url
        img_string = f'<img src="{img_url}" alt="{self.title}" height="200">'
        return mark_safe(img_string)

    def __str__(self):
        return f'{self.title} / Price: {self.real_price} / Count: {self.count}'


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

    @property
    def cost(self):
        return '$' + "{:.2f}".format((self.count * self.product.price) / 100)

    def __str__(self):
        return f'{self.product.title} / Cost: {self.cost} / Count:' \
               f' {self.count} / User: {self.user.full_name}'

    def save(self, *args, **kwargs):
        if self.count <= self.product.count:
            self.user.purse -= self.count * self.product.price
            self.product.count -= self.count
            self.user.save()
            self.product.save()
        else:
            raise ValueError('not enough products for order')
        super(Purchase, self).save(*args, **kwargs)


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

    def __str__(self):
        return f'{self.purchase.product.title} ' \
               f'/ Cost: {self.purchase.cost} ' \
               f'/ Count: {self.purchase.count} ' \
               f'/ User: {self.purchase.user.full_name}' \
               f'/ {self.created_at}'
