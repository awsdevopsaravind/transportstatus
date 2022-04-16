from django import template
register = template.Library()



@register.filter
def tax_amount(value1):
    return round((value1 /100) *5, 2)