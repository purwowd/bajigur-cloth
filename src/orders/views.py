from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import datetime

from orders.models import Order, OrderItem
from products.models import Product
from shippings.models import ShippingAddr
from .decorators import unauthenticated_user


def handler500(request):
    return HttpResponse("Sorry. It's not You. It's Us. Please back to Home", status=500)


@login_required(login_url='auth')
def cart(request):
    if request.user.is_authenticated:
        account = request.user.account
        order, created = Order.objects.get_or_create(
            account=account, complete=False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'orders/cart.html', context)


@login_required(login_url='auth')
def checkout(request):
    if request.user.is_authenticated:
        account = request.user.account
        order, created = Order.objects.get_or_create(
            account=account, complete=False
        )
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        items = []
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cart_items': cart_items}
    return render(request, 'orders/checkout.html', context)


@login_required(login_url='auth')
def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print('action:', action)
    print('product_id:', product_id)

    account = request.user.account
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(
        account=account, complete=False
    )
    order_item, created = OrderItem.objects.get_or_create(
        order=order, product=product
    )

    if action == 'add':
        order_item.quantity = (order_item.quantity + 1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)


@login_required(login_url='auth')
def process_order(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        account = request.user.account
        order, created = Order.objects.get_or_create(
            account=account,
            complete=False
        )
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping:
            ShippingAddr.objects.create(
                account=account,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User is not login...')

    return JsonResponse('Payment complete!', safe=False)
