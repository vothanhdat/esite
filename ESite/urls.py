"""ESite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from graphene_django.views import GraphQLView

import debug_toolbar


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    url(r'hitcount/', include('hitcount.urls', namespace='hitcount')),
    url(r'^weblog/', include('zinnia.urls')),
    url(r'^comments/', include('django_comments.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^', include('econ.urls')),
    url(r'^graphql', GraphQLView.as_view(graphiql=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls)),



# if settings.DEBUG:
#     import debug_toolbar
#     urlpatterns += url(r'^__debug__/', include(debug_toolbar.urls))

