
from django.contrib import admin
from django.template.loader import render_to_string
from django.template.response import TemplateResponse, SimpleTemplateResponse




IS_POPUP_VAR = '_popup'
RANDOM_VAR = '_random'

class CustomAdminPopup(admin.ModelAdmin):
  
  def get_popup_context(self,request,obj):
    """Retrieve context from request and model instance"""
    pass
       
  def popup_response(self,request,obj):
    to_id = request.GET.get(RANDOM_VAR)
    return TemplateResponse(request, "custom/custom_admin_popup_res.html", {
      'to_id' : to_id,
      'object': render_to_string( 
          self.popup_response_template,
          self.get_popup_context(request,obj)
      )
    })

  def response_change(self, request, obj):
    if IS_POPUP_VAR in request.POST:
      return self.popup_response(request,obj)
    else:
      return super(CustomAdminPopup,self).response_change(request, obj)

  def response_add(self, request, obj, post_url_continue=None):
    if IS_POPUP_VAR in request.POST:
      return self.popup_response(request,obj)
    else:
      return super(CustomAdminPopup,self).response_add(request, obj, post_url_continue)