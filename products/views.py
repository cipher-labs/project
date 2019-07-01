from __future__ import unicode_literals
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from shopping_cart.models import Order
from .models import Product,Category,ProductImage
from .mixins import ProductManagerMixin
from cart.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin,
			SubmitBtnMixin
			)
from sellers.mixins import SellerAccountMixin
from .forms import ProductAddForm, ProductModelForm
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView




class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		seller = self.get_account()
		form.instance.seller = seller
		valid_data = super(ProductCreateView, self).form_valid(form)
		#tags = form.cleaned_data.get("tags")
		# if tags:
		# 	tags_list = tags.split(",")
		# 	for tag in tags_list:
		# 		if not tag == " ":
		# 			new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
		# 			new_tag.products.add(form.instance)
		return valid_data

class ProductUpdateView(ProductManagerMixin,SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Update Product"
	def get_initial(self):
		initial = super(ProductUpdateView,self).get_initial()
		print (initial)
		# tags = self.get_object().tag_set.all()
		# initial["tags"] = ", ".join([x.title for x in tags])
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		return initial
	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		# tags = form.cleaned_data.get("tags")
		# obj = self.get_object()
		# obj.tag_set.clear()
		# if tags:
		# 	tags_list = tags.split(",")
        #
		# 	for tag in tags_list:
		# 		if not tag == " ":
		# 			new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
		# 			new_tag.products.add(self.get_object())
		return valid_data

class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(name__icontains=query)|
					Q(description__icontains=query)
				).order_by("name")
		return qs

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
