from django.db import models
from .Promotion import Promotion
from .Agency import Agency
class AgencyPromotion(Promotion):
    apply_to = models.ForeignKey(Agency, on_delete=models.CASCADE)
    
