from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shopping_cart.models import Order
from .models import Product

@login_required
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "products/product_list.html", context)



def single(request,slug):
    product = Product.objects.get(slug=slug)
    images = product.productimage_set.all()
    categories = product.category_set.all()
    if request.user.is_authenticated():
        downloadable = check_product(request.user,product)
    edit = True
    related = []
    if len(categories) >=1:
        for category in categories:
            products_category = category.products.all()
            for item in products_category:
                if not item == product:
                    related.append(item)
    context = {
        "product":product,
        "categories":categories,
        "edit":True,
        "images":images,
        "related":related,
        "downloadable":downloadable,
    }
    return render(request,"products/single.html",context)
