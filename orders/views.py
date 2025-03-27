import datetime
from django.shortcuts import redirect, render
from carts.models import CartItem
from .models import Payment, Order, OrderProduct
from .forms import OrderForm

import json
from django.conf import settings

from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
from django.http import JsonResponse






def payments(request):
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
    grand_total = total + tax

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
            data.order_total = total  # ✅ Fix: Assign order total before saving
            data.grand_total = grand_total
            data.tax = tax
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  #  Save the order before assigning the order number

            # Generate order number
            current_date = datetime.date.today().strftime("%Y%m%d")
            order_number = f"{current_date}{data.id}"  #  Now `data.id` exists
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)

            context = {
                'order': order,
                'cart_items': cart_items,  # ✅ Fix: Use `cart_items` instead of `cart_item`
                'total': total,
                'tax': tax,
                'grand_total': grand_total
            }

            return render(request, 'orders/payments.html', context)
    else:
        return redirect('checkout')
    



def initiate_payment(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    # Initialize SSLCommerz Payment Session
    sslcz = SSLCSession(
        sslc_is_sandbox=settings.SSL_COMMERZ['sandbox'],
        sslc_store_id=settings.SSL_COMMERZ['store_id'],
        sslc_store_pass=settings.SSL_COMMERZ['store_pass']
    )

    # Set transaction parameters
    sslcz.set_urls(
        success_url=request.build_absolute_uri('/payment/success/'),
        fail_url=request.build_absolute_uri('/payment/fail/'),
        cancel_url=request.build_absolute_uri('/payment/cancel/'),
        ipn_url=request.build_absolute_uri('/payment/ipn/')
    )

    sslcz.set_product_integration(
        total_amount=Decimal(order.grand_total),
        currency="BDT",
        product_category="Ecommerce",
        product_name="Order Payment",
        num_of_item=1,
        shipping_method="NO"
    )

    sslcz.set_customer_info(
        name=order.first_name + " " + order.last_name,
        email=order.email,
        address1=order.address_line_1,
        address2=order.address_line_2,
        city=order.area,
        postcode="1200",
        country="Bangladesh",
        phone=order.phone
    )

    sslcz.set_shipping_info(
        shipping_method="Courier",
        num_of_item=1,
        name="Ecommerce Store",
        address="Dhaka",
        city="Dhaka",
        postcode="1200",
        country="Bangladesh"
    )

    response = sslcz.init_payment()
    return redirect(response['GatewayPageURL'])



from django.http import JsonResponse
from orders.models import Order

def payment_success(request):
    return JsonResponse({'message': 'Payment Successful'})

def payment_fail(request):
    return JsonResponse({'message': 'Payment Failed'})

def payment_cancel(request):
    return JsonResponse({'message': 'Payment Cancelled'})
