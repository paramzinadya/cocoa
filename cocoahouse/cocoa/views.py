from calendar import month
from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
import uuid
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy

from cocoa.forms import AddPostForm, UploadFileForm
from cocoa.models import Post, Category, TagPost, Filial, UploadFiles
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from django.views.generic.edit import DeleteView
from django.core.paginator import Paginator

from cocoa.utils import DataMixin
from users.forms import CommentForm

main_menu = [{'title': "О сайте", 'url_name': 'about'},
 {'title': "Каталог", 'url_name': 'catalog'},
 {'title': "Сезонное меню", 'url_name': 'seasons'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Добавить пост", 'url_name': 'addpage'}
]
class CocoaHome(DataMixin, ListView):
    template_name = 'cocoa/index.html'
    context_object_name = 'posts'
    #paginate_by = 3

    def get_context_data(self, *, object_list=None,**kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title = 'Главная страница',cat_selected = 0,)

    def get_queryset(self):
        return Post.published.all().select_related('cat')

class CocoaCategory(DataMixin, ListView):
    template_name = 'cocoa/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected = cat.id,)

    def get_queryset(self):
        return Post.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

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

@login_required
def about(request):
    contact_list = Post.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if request.method == "POST":
        form = UploadFileForm(request.POST,request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()
    return render(request, 'cocoa/about.html', {'page_obj':page_obj, 'title': 'О сайте', 'main_menu': main_menu})

def catalog(request):
 return render(request, 'cocoa/catalog.html',{'title': 'Каталог', 'main_menu': main_menu})

def seasons(request):
 return HttpResponse("Сезонное меню")

@permission_required(perm='cocoa.view_cocoa',raise_exception=True)
def contact(request):
 return HttpResponse("Обратная связь")

def login(request):
 return HttpResponse("Вход в аккаунт")

class TagPostList(DataMixin, ListView):
    template_name = 'cocoa/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    def get_queryset(self):
        return Post.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

class ShowPost(DataMixin, DetailView):
 model = Post
 template_name = 'cocoa/post.html'
 slug_url_kwarg = 'post_slug'
 context_object_name = 'post'

 def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     post = context['post']
     context = self.get_mixin_context(context, title=post.title)
     context['comments'] = post.comments.all().order_by('-created')
     context['form'] = CommentForm()
     context['liked'] = self.request.user in post.likes.all()
     return context

 def post(self, request, *args, **kwargs):
     self.object = self.get_object()
     post = self.object

     # Лайк
     if 'like' in request.POST:
         if request.user.is_authenticated:
             if request.user in post.likes.all():
                 post.likes.remove(request.user)
             else:
                 post.likes.add(request.user)
         return redirect('post', post_slug=post.slug)

     # Комментарий
     if 'comment' in request.POST:
         form = CommentForm(request.POST)
         if form.is_valid() and request.user.is_authenticated:
             comment = form.save(commit=False)
             comment.post = post
             comment.author = request.user
             comment.save()
         return redirect('post', post_slug=post.slug)

     return redirect('post', post_slug=post.slug)

 def get_object(self, queryset=None):
     return get_object_or_404(Post.published,slug=self.kwargs[self.slug_url_kwarg])

class AddPage(PermissionRequiredMixin, LoginRequiredMixin, DataMixin, FormView):
 form_class = AddPostForm
 template_name = 'cocoa/addpage.html'
 success_url = reverse_lazy('home')
 permission_required = 'cocoa.add_post'
 def form_valid(self, form):
     w = form.save(commit=False)
     w.author = self.request.user
     w.save()  # <--- вот этого не хватало
     return super().form_valid(form)


class UpdatePage(DataMixin, UpdateView):
 model = Post
 fields = ['title', 'content', 'photo', 'is_published', 'cat']
 template_name = 'cocoa/addpage.html'
 title_page = 'Редактирование статьи'
 success_url = reverse_lazy('home')

class DeletePage(DataMixin, DeleteView):
    model = Post
    template_name = 'cocoa/delete_confirm.html'
    success_url = reverse_lazy('home')

def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Post.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'main_menu': main_menu,
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
