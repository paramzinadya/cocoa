from django import template

register = template.Library()

@register.inclusion_tag('cocoa/includes/menu_categories.html')
def show_categories():
    menu_items = [
        {"name": "Какао", "url": "category_cacao"},
        {"name": "Горячие напитки", "url": "category_hot_drinks"},
        {"name": "Холодные напитки", "url": "category_cold_drinks"},
        {"name": "Выпечка", "url": "category_baking"},
        {"name": "Десерты", "url": "category_desserts"},
        {"name": "Мерч", "url": "category_merch"},
        {"name": "Подарочные наборы", "url": "category_gift_sets"}
    ]
    return {"menu_items": menu_items}
