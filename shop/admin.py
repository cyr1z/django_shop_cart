from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from .models import Product, ShopUser, Purchase, Return


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ["preview"]

    def preview(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" height="200">')


admin.site.register(Product, ProductAdmin)
admin.site.register(ShopUser)
admin.site.register(Purchase)
admin.site.register(Return)
