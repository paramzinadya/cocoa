from calendar import month
from datetime import datetime
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
import uuid
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from cocoa.forms import AddPostForm, UploadFileForm
from cocoa.models import Post, Category, TagPost, Filial

main_menu = [{'title': "О сайте", 'url_name': 'about'},
 {'title': "Каталог", 'url_name': 'catalog'},
 {'title': "Сезонное меню", 'url_name': 'seasons'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Войти", 'url_name': 'login'},
 {'title': "Добавить пост", 'url_name': 'addpage'}
]

def index(request):
 posts = Post.published.all()
 data = {
 'title': 'Главная страница',
 'main_menu': main_menu,
 'posts': posts,
 'cat_selected': 0,
 }
 return render(request, 'cocoa/index.html', context=data)

def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
        suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data['file'])
    else:
        form = UploadFileForm()
    return render(request, 'cocoa/about.html',{'title': 'О сайте', 'menu': menu, 'form': form})

def catalog(request):
 return render(request, 'cocoa/catalog.html',{'title': 'Каталог', 'main_menu': main_menu})

def seasons(request):
 return HttpResponse("Сезонное меню")

def contact(request):
 return HttpResponse("Обратная связь")

def login(request):
 return HttpResponse("Вход в аккаунт")


def show_post(request, post_slug):
 post = get_object_or_404(Post, slug=post_slug)
 data = {
 'title': post.title,
 'menu': menu,
 'post': post,
 'cat_selected': 1,
 }
 return render(request, 'cocoa/post.html',
context=data)

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'cocoa/index.html', context=data)


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

def show_category(request, cat_slug):
 category = get_object_or_404(Category,slug=cat_slug)
 posts = Post.published.filter(cat_id=category.pk)
 data = {
 'title': f'Рубрика: {category.name}',
 'menu': menu,
 'posts': posts,
 'cat_selected': category.pk,
 }
 return render(request, 'cocoa/index.html',
context=data)


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

def addpage(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        # НЕ создаём заново form в этом else!
    else:
        form = AddPostForm()  # ← создаём форму при GET

    return render(request, 'cocoa/addpage.html', {
        'main_menu': menu,
        'title': 'Добавление статьи',
        'form': form
    })