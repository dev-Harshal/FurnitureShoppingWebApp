from django.contrib import admin
from .models import *
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name' , 'email' , 'role')
admin.site.register(User,UserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('prod_id', 'prod_category', 'prod_title', 'seller_name','prod_price','prod_stock')
admin.site.register(Product,ProductAdmin)

admin.site.register(Cart)
admin.site.register(CartItem)
