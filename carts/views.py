from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Cart, CartItem, TaxSetting
from store.models import Product,Variation
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.


def _cart_id(request):
    """
    Retrieves the session ID of the user.
    If no session exists, it creates a new session.
    Returns the session key to uniquely identify the cart.
    """
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    """
    Adds a product to the cart. If the cart does not exist, creates a new cart.
    If the product already exists in the cart, increases its quantity.
    """
    product = get_object_or_404(Product, id=product_id)
    
    product_variation = []
    if request.method == "POST":
        for key, value in request.POST.items():
            if key not in ["csrfmiddlewaretoken"]:  # Exclude unwanted keys
                try:
                    variation = Variation.objects.get(
                        product=product,
                        variation_category__iexact=key,
                        variation_value__iexact=value
                    )
                    product_variation.append(variation)
                except Variation.DoesNotExist:
                    pass

    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)

    if product_variation:
        cart_item.variations.clear()
        cart_item.variations.add(*product_variation)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    messages.success(request, f"{product.name} was added to your cart!")
    return redirect('cart')






def cart(request, total=0, quantity=0, cart_items=None):
    """ View to display the shopping cart details """
    try:
        # Retrieve the cart using the session ID
        cart = Cart.objects.get(cart_id=_cart_id(request))  

        # Get all active cart items associated with this cart
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        # Loop through each cart item to calculate total price and quantity
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)  # Calculate total price
            quantity += cart_item.quantity  # Calculate total quantity of items in cart

         # Get dynamic tax percentage from database
        tax_setting = TaxSetting.objects.first()  # Get the first tax setting
        tax_percentage = tax_setting.tax_percentage if tax_setting else 2  # Default to 2% if not set

        # Calculate tax dynamically
        tax = (tax_percentage * total) / 100
        grand_total = total + tax
        

    except ObjectDoesNotExist:
        # If the cart doesn't exist, do nothing and avoid errors
        pass  

    # Prepare context data to send to the template
    context = {
        'total': total,        # Total cart price
        'quantity': quantity,  # Total quantity of products in cart
        'cart_items': cart_items,  # List of all cart items
        'tax' :tax,
        'grand_total':grand_total
    }

    # Render the 'cart.html' template and pass the cart data
    return render(request, 'store/cart.html', context)


def remove_cart(request, product_id):
    """ Decrease quantity of a product in the cart or remove it if quantity is 1 """
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the user's cart
    product = get_object_or_404(Product, id=product_id)  # Get the product

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1  # Reduce quantity by 1
            cart_item.save()
        else:
            cart_item.delete()  # Remove item from cart if quantity is 1
        
    except CartItem.DoesNotExist:
        pass  # Ignore if no such cart item exists

    return redirect('cart')  # Redirect back to cart page


def remove_cart_item(request, product_id):
    """ Completely remove a product from the cart """
    cart = Cart.objects.get(cart_id=_cart_id(request))  # Get the user's cart
    product = get_object_or_404(Product, id=product_id)  # Get the product

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.delete()  # Delete the item completely
    except CartItem.DoesNotExist:
        pass  # Ignore if no such cart item exists

    return redirect('cart')  # Redirect back to cart page
