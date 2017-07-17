
from django_mptt_admin.admin import DjangoMpttAdmin
from django.contrib import admin
from ..models import Cagetory


@admin.register(Cagetory)
class CagetoryAdmin(DjangoMpttAdmin):
  tree_auto_open = False