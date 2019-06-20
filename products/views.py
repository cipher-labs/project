from __future__ import unicode_literals
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from shopping_cart.models import Order
from .models import Product,Category,ProductImage

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
    related = []
    if len(categories) >=1:
        for category in categories:
            products_category = category.product.all()
            for item in products_category:
                if not item == product:
                    related.append(item)
    context = {
        "product":product,
        "categories":categories,
        "edit":True,
        "images":images,
        "related":related,
    }
    return render(request,"products/single.html",context)


def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
    if q:
        query = q

    product_queryset = Product.objects.filter(
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    category_queryset = Category.objects.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)
    )
    results = list(chain(product_queryset,category_queryset))
    """

    if q:
        query = "You searched for: %s" %(q)
        k = q.split()
        if len(k)>=2:
            products = []
            for item in k:
                all_products = Product.objects.filter(title__icontains=item).distinct()
                for product in all_products:
                    products.append(product)
        else:
            products = Product.objects.filter(title__icontains=q)
            """
    context = {
        'query':query,
        'product_queryset':product_queryset,
        'category_queryset':category_queryset,
        'results':results,
    }

    return render(request,"products/search.html", context)

def category_single(request,slug):
    try:
        category = Category.objects.get(slug=slug)
    except:
        raise Http404
    products = category.product.all()
    related = []
    for item in products:
        product_categories = item.category_set.all()
        for single_category in product_categories:
            if not single_category == category:
                related.append(single_category)
    context = {
        'category':category,
        'products':products,
        'related':related,
    }
    return render(request,"products/category.html",context)
