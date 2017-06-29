from django.contrib import admin
from .models import Brand,Cagetory,Product,ProductImage


class ProductImageInLine(admin.StackedInline):
  model = ProductImage
  fields = ['image']

class PostProduct(admin.ModelAdmin):
    inlines = [ProductImageInLine]


admin.site.register(Brand)
admin.site.register(Cagetory)
admin.site.register(Product,PostProduct)