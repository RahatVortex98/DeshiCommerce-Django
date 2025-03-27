from .models import Cart, CartItem
from .utils import _cart_id  # Import _cart_id from utils

def counter(request):
    cart_count = 0  

    if 'admin' in request.path:
        return {}

    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart_id = _cart_id(request)  # Get cart_id from session
            cart, created = Cart.objects.get_or_create(cart_id=cart_id)  # Create if not exist
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        cart_count = sum(item.quantity for item in cart_items)

    except Exception as e:
        print("Cart Error:", e)  # Debugging purpose
        cart_count = 0  

    return {'cart_count': cart_count}
