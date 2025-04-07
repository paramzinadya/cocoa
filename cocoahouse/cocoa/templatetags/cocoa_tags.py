from django import template
import cocoa.views as views
from cocoa.models import Category

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
 return Category.objects.all()

@register.inclusion_tag('cocoa/list_categories.html')
def show_categories(cat_selected_id=0):
 cats = Category.objects.all()
 return {"cats": cats, "cat_selected":cat_selected_id}

