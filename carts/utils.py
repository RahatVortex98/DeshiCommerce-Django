import uuid

def _cart_id(request):
    cart_id = request.session.get('cart_id')
    if not cart_id:
        request.session['cart_id'] = str(uuid.uuid4())  # Generate a unique ID
        cart_id = request.session['cart_id']
    return cart_id
