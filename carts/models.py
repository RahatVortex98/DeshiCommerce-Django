from django.db import models
from accounts.models import Account


# Avoid direct import to prevent circular import issues
# from store.models import Product, Variation  



class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name="items", null=True)
    
    # Use lazy string references to avoid import errors
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE)
    variations = models.ManyToManyField('store.Variation', blank=True)

    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class TaxSetting(models.Model):
    tax_percentage = models.FloatField(default=2)  # Default is 2%

    def __str__(self):
        return f"Tax: {self.tax_percentage}%"
