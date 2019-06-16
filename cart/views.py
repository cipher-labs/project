import os
from django.conf import settings
from django.shortcuts import render
from shopping_cart.models import Order
from products.models import Featured

# def home(request):
#     featured_products = []
#     featured = Featured.objects.all()
#     for i in featured_products:
#         featured_products.append(i)
#     template= "home.html"
#     context={}
#     return render(request,template,context)
def home(request):
    featured_products = []
    featured = Featured.objects.get_featured_instance()
    for i in featured.products.all():
        featured_products.append(i)
    try:
        order_id = request.session['order_id']
        cart = Order.objects.get(id=order_id)
    except:
        in_cart = False
        orderitems = None
    # if cart:
    #     cartitems = []
    #     for item in cart.cartitem_set.all():
    #         cartitems.append(item.product)
    template= "home.html"
    context={
        'featured_products':featured_products,
        'featured':featured
    }
    return render(request,template,context)
