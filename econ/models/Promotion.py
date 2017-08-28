from django.db import models

class Promotion(models.Model) : 
    PROMOTION_TYPE = (
        ('M','Minus'), 
        ('P','Percentage'), 
        ('O','Offer'), 
    )
    name = models.CharField(max_length=100)
    promotiontype = models.CharField(max_length=1, choices=PROMOTION_TYPE,default='P')
    value = models.FloatField()
    start = models.DateTimeField(null=True)
    end = models.DateTimeField(null=True)
    # promotion_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name
