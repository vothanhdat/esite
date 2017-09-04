
from django.db.models import Sum, Count, When,F,Q, Case,IntegerField, DurationField, ExpressionWrapper, Value, DateTimeField, Func
from econ.models import Product
from django.utils import timezone
from datetime import datetime
from django.db.models.functions  import ExtractDay,
class Date(Func):
    '''
    Custom query expression to get date from datetime object.
    Example usage
    queryset.annotate(
        created_at=Date('created_at')
    )
    '''
    function = 'DATE'

a = Product.objects.all()


def duration_string(duration):
    days = duration.days
    seconds = duration.seconds
    microseconds = duration.microseconds
    minutes = (seconds // 60)
    seconds = (seconds % 60)
    hours = (minutes // 60)
    minutes = (minutes % 60)
    string = '{:02d}:{:02d}:{:02d}'.format(hours, minutes, seconds)
    if days:
        string = '{} '.format(days) + string
    else:
        pass
    return string



# a.filter(isvariety=1).annotate(
#     qua=Sum('productoption__quatity'),
#     count=Count('productoption')
# ).values('qua','count')

# c = a.annotate(
#     qua=Sum('productoption__quatity'),
#     count=Case(
#         When(isvariety=1, then=Count('productoption')),
#         default=F('quatity'),
#         output_field=IntegerField(),
#     ),
# ).prefetch_related('productoption_set')


# d = a.annotate( last_update= Value(timezone.now()) - F('modified')).values('last_update')
# d = a.annotate( last_update= Value(timezone.now()) - F('modified')).values('last_update')
# d = a.annotate( last_update= Value(timezone.now(),output_field=DateTimeField())).values('last_update')

a.annotate( 
    last_update=ExpressionWrapper(
        Value(
            timezone.now(),
            output_field=DateTimeField()
        ) - F('modified'),
        output_field=DurationField()
    )
).values('last_update')


a.annotate( 
    last_update=ExtractDay(
        Value(
            timezone.now(),
            output_field=DateTimeField()
        ) - F('modified'),
    )
).values('last_update')