from django.conf.urls import url

from .views import index,product,autocomplete

app_name = 'econ'
urlpatterns = [
    url(r'^product/$', index.index, name='index'),
    url(r'^product/(?P<product_id>[0-9]+)/$', product.index, name='product'),
    url(r'^cagetory/(?P<cagetory_id>[0-9]+)/$', index.indexbycagetory, name='cagetory'),
    url(r'^$', index.index, name='index'),
] + autocomplete.urlpatterns

