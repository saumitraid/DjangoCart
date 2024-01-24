from django.contrib import admin
from .models import Product, CartItem
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def prd_image(self, obj):
        return format_html('<img src="{}" width="50" height="50"/>'.format(obj.image.url))
    
    list_display=('name','description','price','prd_image')

admin.site.register(CartItem)