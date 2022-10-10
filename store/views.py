from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime             # To generate transaction ID               

from .models import *

def store(request):

    if request.user.is_authenticated:
        customer = request.user.customer                # a user who is a customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)         # a list of all 'incomplete' order by a 'customer'
        items = order.orderitem_set.all()              
        cartItems = order.get_cart_items
    else:
        items = []                          
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']


    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer                # a user who is a customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)         # a list of all 'incomplete' order by a 'customer'
        items = order.orderitem_set.all()              # .<(lowercase)modelName>_set.all(): gives all orderitems which is part of a particular order(identified by abobe cond.)
        cartItems = order.get_cart_items
    else:
        # return to login/signup page
        items = []                          # will take care of it later!
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    
    if request.user.is_authenticated:
        customer = request.user.customer                # a user who is a customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)         # a list of all 'incomplete' order by a 'customer'
        items = order.orderitem_set.all()              # .<(lowercase)modelName>_set.all(): gives all orderitems which is part of a particular order(identified by abobe cond.)
        cartItems = order.get_cart_items
    else:
        # return to login/signup page
        items = []                          # will take care of it later!
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping':False}
        cartItems = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)                 # Parsing json string to a dict of data sent by cart.js
    productId = data['productId']
    action = data['action']
    
    print('ProductId:', productId, 'Action:', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)         # a list of all 'incomplete' order by a 'customer'

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added!', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M')
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        transaction_id += '_' + str(order.id)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shipping']['address'],
                city = data['shipping']['city'],
                state = data['shipping']['state'],
                zipcode = data['shipping']['zipcode'],
            )
        # Re defining data to use it in html mail form!            
        data['form']['name'] = customer
        data['form']['email'] = customer.email
        mail(data, transaction_id, order)                   #
    else:
        print('User is not logged in!')             # Prompt!
    # print('Data: ', request.body)
    return JsonResponse('Payment Complete!', safe=False)

from django.conf import Settings
from django.core.mail import EmailMessage
from django.template.loader import render_to_string 
def mail(data, transaction_id, order):          
    # since we only have one seller: we dont need any loop to add multiple sellers to a list and loop the email through!

    # Product
    items = OrderItem.objects.filter(order=order.id)            # Dict of products in a order!

    template = render_to_string('store/email_template.html', {
        'data': data, 
        'transaction_id': transaction_id, 
        'items': items,
    })
    subject = 'Order details of Order No: ' + transaction_id
    
    email = EmailMessage(
        subject,
        template,             # template
        '',                     # Email host user!
        ['' ],      # This list should have: seller mail-id!
    )
    email.fail_silently = False
    email.send()
    #123@Owner