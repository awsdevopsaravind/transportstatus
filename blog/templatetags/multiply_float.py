from django import template
register = template.Library()



@register.filter
def multiply_float(value1,value2):
    return round(value1 * value2 , 2)