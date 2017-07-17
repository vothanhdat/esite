from django.contrib import admin
from ..models import ProductPromotion


@admin.register(ProductPromotion)
class PromotionAdmin(admin.ModelAdmin):
    pass