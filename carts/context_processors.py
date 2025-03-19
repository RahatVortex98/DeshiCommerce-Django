from .models import Cart, CartItem  # Import the Cart and CartItem models
from .views import _cart_id  # Import the function that generates a unique cart ID

def counter(request):
    cart_count = 0  # Initialize cart_count to zero

    # If the request is coming from the admin panel, return an empty dictionary (no need to count)
    if 'admin' in request.path:
        return {}

    else:
        try:
            #  Get the cart associated with the current session
            cart = Cart.objects.filter(cart_id=_cart_id(request))

            #  Get all cart items for this cart (but only take the first cart found)
            cart_items = CartItem.objects.all().filter(cart=cart[:1])

            #  Loop through each cart item and count the total quantity of products
            for cart_item in cart_items:
                cart_count += cart_item.quantity

        except Cart.DoesNotExist:
            #  If the cart doesn't exist, set count to 0
            cart_count = 0  

    #  Return the count as a dictionary (so it can be used in templates)
    return dict(cart_count=cart_count)
