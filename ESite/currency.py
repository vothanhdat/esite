from decimal import ROUND_HALF_EVEN
import moneyed
from moneyed.localization import _FORMATTER


VND = moneyed.add_currency(
    code='VND',
    numeric='084',
    name='Vietnam Dong',
    countries=('Viet Nam', )
)

# Currency Formatter will output 2.000,00 Bs.
_FORMATTER.add_sign_definition(
    'default',
    VND,
    suffix=u' .VND',

)

_FORMATTER.add_formatting_definition(
    'vi_VN',
    group_size=3, group_separator=".", decimal_point=",",
    positive_sign="",  trailing_positive_sign="",
    negative_sign="-", trailing_negative_sign="",
    rounding_method=ROUND_HALF_EVEN
)