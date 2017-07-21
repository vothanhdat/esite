from django.conf.urls import url, include

from .views import index,product,autocomplete,setting,password,slug

app_name = 'econ'
urlpatterns = [
    url(r'^product/$', index.index, name='index'),
    url(r'^product/(?P<product_id>[0-9]+)/$', product.index, name='product'),
    url(r'^cagetory/(?P<cagetory_id>[0-9]+)/$', index.indexbycagetory, name='cagetory'),
    url(r'^brand/(?P<brand_id>[0-9]+)/$', index.indexbybrand, name='brand'),
    url(r'^accounts/$', setting.index, name='settings'),
    url(r'^accounts/profile/$', setting.index, name='settings'),
    url(r'^settings/$', password.index, name='password'),
    url(r'^autocomplete/', include(autocomplete.urlpatterns), name='auto-complete'),
    url(r'^$', index.index, name='index'),
    url(r'^(?P<slug>[\w-]+)/$', slug.index, name='slug'),
]

