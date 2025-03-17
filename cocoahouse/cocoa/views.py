from calendar import month
from datetime import datetime
from django.template.loader import render_to_string


from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

main_menu = [{'title': "О сайте", 'url_name': 'about'},
 {'title': "Каталог", 'url_name': 'catalog'},
 {'title': "Сезонное меню", 'url_name': 'seasons'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Войти", 'url_name': 'login'}
]

data_db = [
 {'id': 1, 'title': 'Фирменное какао', 'content': 'Наше какао — это уют в каждой чашке! Богатый шоколадный вкус, нежная текстура и согревающий аромат делают его идеальным напитком для любого момента. Попробуйте и ощутите настоящее наслаждение!', 'is_published': True},
 {'id': 2, 'title': 'Свежая выпечка', 'content': 'Хрустящие круассаны, мягкие булочки и ароматные пирожки — каждое утро мы готовим свежую выпечку для вас! Заходите за теплом и вкусом прямо из печи.', 'is_published': True},
 {'id': 3, 'title': 'Любимые десерты', 'content': 'Торты, эклеры, чизкейки — у нас есть десерт для каждого сладкоежки! Побалуйте себя любимыми вкусами и окунитесь в мир удовольствия.', 'is_published': True},
]

cats_db = [
 {'id': 1, 'name': 'Акции'},
 {'id': 2, 'name': 'Подарки'},
 {'id': 3, 'name': 'Адреса'},
 {'id': 4, 'name': 'Соц.сети'},
]

def index(request):
 data = {
     'title': 'COCOA HOUSE',
     'main_menu': main_menu,
     'posts': data_db,
 }
 return render(request, 'cocoa/index.html', context=data)

def about(request):
 return render(request, 'cocoa/about.html',{'title': 'О сайте', 'main_menu': main_menu})

def catalog(request):
 return render(request, 'cocoa/catalog.html',{'title': 'Каталог', 'main_menu': main_menu})

def seasons(request):
 return HttpResponse("Сезонное меню")

def contact(request):
 return HttpResponse("Обратная связь")

def login(request):
 return HttpResponse("Вход в аккаунт")

def show_post(request, post_id):
 return HttpResponse(f"Отображение статьи с id ={post_id}")

def menu(request):
    return HttpResponse(f"<h1>Меню</h1>")

#ТУТ НОВЫЕ
def category_cacao(request):
 return HttpResponse("Сорта какао")

def category_hot_drinks(request):
 return HttpResponse("Горячие напитки")

def category_cold_drinks(request):
 return HttpResponse("Холодные напитки")

def category_baking(request):
 return HttpResponse("Выпечка")

def category_desserts(request):
 return HttpResponse("Выпечка")

def category_merch(request):
 return HttpResponse("Мерч")

def category_gift_sets(request):
 return HttpResponse("Подарочные наборы")


def show_category(request, cat_id):
 """Функция-заглушка"""
 return index(request)

def menu_slug(request,cat_slug):
    if request.GET:
        print(request.GET)
    if request.POST:
        print(request.POST)
    if cat_slug == 'main':
        return redirect ('home',permanent=True)
    return HttpResponse(f"<h1>Категории меню </h1><p >категория меню с названием:{ cat_slug }</p>")

def get_season(month):
    if month in [12, 1, 2]:
        return "зиму"
    elif month in [3, 4, 5]:
        return "весну"
    elif month in [6, 7, 8]:
        return "лето"
    elif month in [9, 10, 11]:
        return "осень"
    return "неизвестный сезон"

def season(request):
    current_month = datetime.now().month
    return redirect(reverse('season_menu', args=[current_month]))  # Перенаправляем на /season/<текущий_месяц>/

def season_menu(request, month):
    season = get_season(month)
    return HttpResponse(f"<h1>Сезонное меню на {season}</h1>")

def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')