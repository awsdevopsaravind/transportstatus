from django import template
register = template.Library()



@register.filter
def total_amount_float(value):
    return round(int(value) , 2)