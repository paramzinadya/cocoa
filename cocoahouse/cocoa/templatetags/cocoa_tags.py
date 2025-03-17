from django import template
import cocoa.views as views

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
 return views.cats_db

