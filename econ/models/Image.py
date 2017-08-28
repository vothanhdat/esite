from django.db import models


class Image(models.Model):
    class Meta:
         abstract = True
    
    image = models.ImageField(upload_to='media/%Y/%m/%d/%H/%M/%S/',null=True, blank=True)
    image_link = models.CharField(max_length=300,null=True, blank=True)
    
    def __str__(self):
        return self.url()

    def url(self):
        if(self.image):
            return self.image.url
        else :
            return self.image_link
