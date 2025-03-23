from django.shortcuts import get_object_or_404
from carts.models import Cart  # This will not cause circular import issues

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
