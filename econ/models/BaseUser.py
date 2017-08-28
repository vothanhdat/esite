from django.db import models
from django.contrib.auth.models import User

class BaseUser(User):
    GENDER = (
        ('U','Unknow'), 
        ('M','Male'), 
        ('F','Female'), 
    )
    bio = models.TextField(max_length=500, blank=True)
    address = models.TextField(max_length=500, blank=True)
    birthday = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER,default='U')
    avatar = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
