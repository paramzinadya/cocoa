from django import template
import cocoa.views as views
from cocoa.models import Category, TagPost, Filial

register = template.Library()

@register.simple_tag(name='getcats')
def get_categories():
 return Category.objects.all()

@register.inclusion_tag('cocoa/list_categories.html')
def show_categories(cat_selected_id=0):
 cats = Category.objects.all()
 return {"cats": cats, "cat_selected":cat_selected_id}

@register.inclusion_tag('cocoa/list_tags.html')
def show_all_tags():
 return {"tags": TagPost.objects.all()}

@register.simple_tag
def get_menu():
 return views.main_menu


