from django.contrib import admin
from ..models import Brand
from .tagged import TagInline

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    inlines=[TagInline]