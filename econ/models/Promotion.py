from django.db import models

class Promotion(models.Model) : 
    PROMOTION_TYPE = (
        ('M','Minus'), 
        ('P','Percentage'), 
        ('O','Offer'), 
    )
    promotion_name = models.CharField(max_length=100)
    promotion_type = models.CharField(max_length=1, choices=PROMOTION_TYPE,default='P')
    promotion_value = models.FloatField()
    promotion_start = models.DateTimeField(null=True)
    promotion_end = models.DateTimeField(null=True)
    # promotion_agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    class Meta:
        abstract = True

    def __str__(self):
        return self.promotion_name
