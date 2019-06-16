from django.conf.urls import url

from .views import (
    product_list,
    single,
    )

app_name = 'products'

urlpatterns = [
    url(r'^', product_list, name='product-list'),
    url(r'^(?P<slug>.*)/$',single,name="single_product"),
]
