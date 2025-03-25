from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderProductInline(admin.TabularInline):  
    model = OrderProduct
    extra = 1  # Allows adding extra items in the admin panel

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'user', 'order_total', 'tax', 'status', 'is_ordered', 'created_at')
    list_filter = ('status', 'is_ordered', 'created_at')
    search_fields = ('order_number', 'user__email', 'first_name', 'last_name', 'phone')
    list_per_page = 20
    inlines = [OrderProductInline]  # Shows related order items inside OrderAdmin

class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'product_price', 'ordered')
    list_filter = ('ordered',)
    search_fields = ('order__order_number', 'product__name')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')

    list_filter = ('payment_method', 'status')
    search_fields = ('payment_id', 'user__email')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
admin.site.register(Payment, PaymentAdmin)
