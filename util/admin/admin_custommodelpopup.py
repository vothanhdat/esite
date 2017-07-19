
from django.contrib import admin
from django.template.loader import render_to_string
from django.template.response import TemplateResponse, SimpleTemplateResponse
from django.core.urlresolvers import reverse
from util.func import rabdombase64




IS_POPUP_VAR = '_popup'
RANDOM_VAR = '_random'

class CustomAdminPopup(admin.ModelAdmin):
  
  def get_popup_context(self,request,obj):
    """Retrieve context from request and model instance"""
    pass
       
  def popup_response(self,request,obj,isnew):
    to_id = request.GET.get(RANDOM_VAR)
    href = reverse(
      'admin:%s_%s_change' % (obj._meta.app_label,  obj._meta.model_name),
      args=(obj.id,)
    )
    return TemplateResponse(request, "custom/custom_admin_popup_res.html", {
      'to_id' : to_id,
      'href' : href,
      'isnew' : 1 if isnew else '',
      'newuuid' : rabdombase64() if isnew else '',
      'object': render_to_string( 
          self.popup_response_template,
          self.get_popup_context(request,obj)
      ),
    })

  def response_change(self, request, obj):
    if IS_POPUP_VAR in request.POST:
      return self.popup_response(request,obj,False)
    else:
      return super(CustomAdminPopup,self).response_change(request, obj)

  def response_add(self, request, obj, post_url_continue=None):
    if IS_POPUP_VAR in request.POST:
      return self.popup_response(request,obj,True)
    else:
      return super(CustomAdminPopup,self).response_add(request, obj, post_url_continue)