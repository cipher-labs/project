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
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]
    # if cart:
    #     cartitems = []
    #     for item in cart.cartitem_set.all():
    #         cartitems.append(item.product)
    template= "home.html"
    context={
        'featured_products':featured_products,
        'featured':featured,
        'current_order_products':current_order_products
    }
    return render(request,template,context)
