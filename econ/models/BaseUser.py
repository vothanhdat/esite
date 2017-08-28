from django.db import models
from django.contrib.auth.models import User

class BaseUser(User):
    GENDER = (
        ('U','Unknow'), 
        ('M','Male'), 
        ('F','Female'), 
    )
    baseuser_bio = models.TextField(max_length=500, blank=True)
    baseuser_address = models.TextField(max_length=500, blank=True)
    baseuser_birthday = models.DateField(null=True, blank=True)
    baseuser_gender = models.CharField(max_length=1, choices=GENDER,default='U')
    baseuser_avatar = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
