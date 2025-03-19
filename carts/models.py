from django.db import models

from store.models import Product, Variation

# Create your models here.
class Cart(models.Model):
    cart_id = models.CharField(max_length=250,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    

    variations = models.ManyToManyField(Variation,blank=True)
    

    is_active = models.BooleanField(default=True)

    

    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"



class TaxSetting(models.Model):
    tax_percentage = models.FloatField(default=2)  # Default is 2%

    def __str__(self):
        return f"Tax: {self.tax_percentage}%"