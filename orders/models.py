from django.db import models
from accounts.models import Account
from store.models import Product, Variation

class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, unique=True)  # Ensure it's unique
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Changed from account_paid
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.payment_id} - {self.status}"
    


class Order(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20, unique=True)  # Ensures unique orders
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)  # Increased length for better international support
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)  # Made optional
    area = models.CharField(max_length=100, blank=True, null=True)  # Made optional
    division = models.CharField(max_length=50, blank=True, null=True)  # Made optional
    order_note = models.TextField(blank=True, null=True)  # Made optional
    order_total = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)   # Changed from FloatField
    tax = models.DecimalField(max_digits=10, decimal_places=2)  # Changed from FloatField
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='New')
    ip = models.GenericIPAddressField(blank=True, null=True)  # Stores proper IP format
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    

    def __str__(self):
        return f"Order {self.order_number} - {self.first_name}"
    
    



class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)  

    color = models.CharField(max_length=50, blank=True, null=True)  # Made optional
    size = models.CharField(max_length=50, blank=True, null=True)  # Made optional
    quantity = models.PositiveIntegerField()  # Ensures non-negative values
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Changed from FloatField
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return f"{self.product.product_name} - {self.quantity} pcs"



    