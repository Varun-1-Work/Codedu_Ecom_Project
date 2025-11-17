from decimal import Decimal
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='login')
def start_payment(request):
    cart = request.session.get('cart', {})
    total = Decimal('0.00')

    for pid, item in cart.items():
        try:
            price = Decimal(item['price'])
        except:
            price = Decimal('0.00')

        qty = item.get('quantity', 0)
        total += price * qty

    amount = int(total * 100)   # convert to paise

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create Razorpay Order
    payment = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": "1"
    })

    # Pass order details to template
    context = {
        "amount": amount,
        "razorpay_order_id": payment["id"],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "total_display": float(total)
    }

    return render(request, "paymentapp/checkout.html", context)


@csrf_exempt
def payment_success(request):
    return render(request, "paymentapp/success.html")
