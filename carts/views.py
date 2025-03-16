from django.shortcuts import get_object_or_404, render

from store.models import Product

# Create your views here.

def add_cart(request,product_id):
    product = get_object_or_404(Product,id=product_id)
    return render(request,'store/cart.html',{'product':product})

def cart(request):
    return render(request,'store/cart.html')