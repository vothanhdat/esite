from django.db import models
from django.utils import timezone



class ModifyLog(models.Model):

    class Meta:
         abstract = True

    created     = models.DateTimeField(editable=False,default=timezone.now)
    modified    = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super(ModifyLog,self).save(*args, **kwargs)


