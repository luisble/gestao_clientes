from django import template

register = template.Library()

@register.filter
def arredonda(value,casas):
    return round(value,casas)

@register.filter
def moeda(value, casas):
    a = '{:,.2f}'.format(float(round(value,casas)))
    b = a.replace(',','v')
    c = b.replace('.',',')
    return c.replace('v','.')