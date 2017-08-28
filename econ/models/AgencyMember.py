from django.db import models
from .Agency import Agency
from .BaseUser import BaseUser

class AgencyMember(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    user = models.ForeignKey(BaseUser, on_delete=models.CASCADE)
    inviter = models.ForeignKey(BaseUser, on_delete=models.CASCADE,related_name="membership_invites",null=True, blank=True)
