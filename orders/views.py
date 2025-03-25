import datetime
from django.shortcuts import redirect, render
from carts.models import CartItem
from .models import Payment, Order, OrderProduct
from .forms import OrderForm





def payments(request):
   def payment(request):
    try:
        order = Order.objects.get(user=request.user, is_ordered=False)
        cart_items = CartItem.objects.filter(user=request.user, is_active=True)

        total = 0
        quantity = 0
        tax = 0
        grand_total = 0

        if cart_items.exists():
            for cart_item in cart_items:
                total += (cart_item.product.price * cart_item.quantity)
                quantity += cart_item.quantity

            tax = (2 * total) / 100
            grand_total = total + tax
        else:
            total = 0
            tax = 0
            grand_total = 0

    except Order.DoesNotExist:
        order = None
        cart_items = None
        total = 0
        tax = 0
        grand_total = 0
          # Debugging: Print retrieved cart items
        print("Cart Items:", cart_items)  
        for item in cart_items:
            print(f"Product: {item.product.name}, Quantity: {item.quantity}")

    context = {
        'order': order,
        'cart_items': cart_items,
        'total': total,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/payment.html', context)




def place_order(request, quantity=0, total=0):
    current_user = request.user

    # If the cart is empty, redirect to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    # Calculate total and tax
    for cart_item in cart_items:
        total += (cart_item.product.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = (2 * total) / 100
    order_total = total + tax

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            # Create and save the order first
            data = Order()
            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line_1 = form.cleaned_data['address_line_1']
            data.address_line_2 = form.cleaned_data['address_line_2']
            data.area = form.cleaned_data['area']
            data.division = form.cleaned_data['division']
            data.order_note = form.cleaned_data['order_note']
            data.order_total = order_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #  Save the order before assigning the order number

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = f"{current_date}{data.id}"  #  Now `data.id` exists
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)

            context ={
                'order':order,
                'cart_item':cart_item,
                'total':total,
                'tax':tax,
                'order_total':order_total
            }

            return render(request,'orders/payments.html',context)
    else:
        return redirect('checkout')
