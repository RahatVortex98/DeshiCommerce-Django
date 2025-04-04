from django.contrib import admin
from .models import Cart, CartItem,TaxSetting



class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','created_at')

class CartItemAdmin(admin.ModelAdmin):
    list_display= ('product','user','cart','quantity','is_active')

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem,CartItemAdmin)

 

admin.site.register(TaxSetting)
