from django.conf.urls import url

from .views import index,product

app_name = 'econ'
urlpatterns = [
    url(r'^$', index.index, name='index'),
    url(r'^product/$', index.index, name='index'),
    url(r'^product/(?P<product_id>[0-9]+)/$', product.index, name='product'),
]