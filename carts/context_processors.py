from .models import Cart, CartItem
from .utils import _cart_id  # Import from utils

def counter(request):
    cart_count = 0  

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        cart_count = sum(item.quantity for item in cart_items)

    except CartItem.DoesNotExist:
        cart_count = 0  

    return {'cart_count': cart_count}
