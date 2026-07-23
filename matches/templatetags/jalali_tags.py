from django import template
import jdatetime
from django.utils import timezone
from zoneinfo import ZoneInfo

register = template.Library()

@register.filter(name='to_jalali')
def to_jalali(value):
    if not value:
        return ""
    # تبدیل به منطقه زمانی تهران
    tehran_time = value.astimezone(ZoneInfo('Asia/Tehran')) if hasattr(value, 'astimezone') else value
    
    # تبدیل تاریخ و ساعت میلادی به جلالی
    j_date = jdatetime.datetime.fromgregorian(datetime=tehran_time)
    
    # فرمت خروجی: مثلاً 1405/05/01 - 15:30
    return j_date.strftime('%Y/%m/%d - %H:%M')