from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Order, Payment
from carts.models import CartItem
from .forms import OrderForm

import datetime
import json

# Create your views here.

def payments(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_ordered=False, order_number=body['orderID'])

    # Store transaction details inside Payment model
    payment = Payment(
         user = request.user,
         payment_id = body['transID'],
         payment_method = body['payment_method'],
         amount_paid = order.order_total,
         status = body['status'],
    )
    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    return render(request, 'orders/payments.html')


def place_order(request, total=0, quantity=0):
    current_user = request.user

    # If count of the products in the cart is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <=0:
        return redirect('store:store')
    
    tax = 0
    # total_after_tax = 0
    total_with_tax = 0
    for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

    tax = (0.5 * total) //100
    # total_after_tax = total - tax
    total_with_tax = total + tax
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # Store all the billing info inside Order table
            data = Order()

            data.user = current_user
            data.first_name = form.cleaned_data['first_name']
            data.last_name = form.cleaned_data['last_name']
            data.phone = form.cleaned_data['phone']
            data.email = form.cleaned_data['email']
            data.address_line = form.cleaned_data['address_line']
            data.order_note = form.cleaned_data['order_note']
            data.ip = request.META.get('REMOTE_ADDR')

            data.order_total = total_with_tax
            data.tax = tax
            data.save()

            # Generate order number
            year = int(datetime.date.today().strftime('%Y'))
            day = int(datetime.date.today().strftime('%d'))
            month = int(datetime.date.today().strftime('%m'))
            date = datetime.date(year, month, day)
            current_date = date.strftime("%Y%m%d")

            # Order number
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()
            
            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'total': total,
                'tax': tax,
                'total_with_tax': total_with_tax,
            }
            
            return render(request, 'orders/payments.html', context)
        
    return redirect('carts:checkout')