from util.admin.admin_custommodelpopup import CustomAdminPopup,RANDOM_VAR
from django.utils.html import format_html_join,format_html
from django.contrib import admin
from util.func import rabdombase64,addparamtourl
from econ.models import ProductOption, Product, ProductOptionImage
from .specificdetail import OptionSpecificDetailInline

class ProductOptionImageInline(admin.TabularInline):
  model = ProductOptionImage

@admin.register(ProductOption)
class ProductOptionAdmin(CustomAdminPopup):
  popup_response_template = "product_option_compact.html"
  inlines = [ProductOptionImageInline, OptionSpecificDetailInline]
  readonly_fields = ('product',)
  fields = ('product','price',)

  def product(self, instance):
    try:
       return format_html('<input value="{}" name="prod" readonly style="display:none;"/><b>{}</b>',instance.prod.id,instance.prod)
    except:
      if self.prod_id:
        prod = Product.objects.get(id=self.prod_id)
        return format_html('<input value="{}" name="prod" readonly style="display:none;"/><b>{}</b>',prod.id,prod)

      return format_html('<input value="11" name="prod" readonly style="display:none;"/><b></b>')

  def get_changeform_initial_data(self, request):
    self.prod_id = request.GET.get('prod',None)
    return super(ProductOptionAdmin,self).get_changeform_initial_data(request)


  def save_form(self, request, form, change):
    prod_id = request.GET.get('prod',None)
    r = super(ProductOptionAdmin, self).save_form(request, form, change)
    if prod_id and not change:
      r.prod_id = prod_id
    return r

  def get_model_perms(self, request):
    return {}

  def get_popup_context(self,request,obj):
    return { 'product' : obj }


