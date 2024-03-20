from django.contrib import admin

# Register your models here.
from .models import Category, Subcategory, Product, User, CartItem
from rest_framework.authtoken.models import Token


class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)


class UserAdmin(admin.ModelAdmin):

    search_fields = ("email",)


# Register your models here.
admin.site.register(User, UserAdmin)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Subcategory)
# admin.site.register(User)
admin.site.register(CartItem)
