from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Post, Category
from datetime import date

class FilialFilter(admin.SimpleListFilter):
 title = 'Наличие филиала'
 parameter_name = 'status'

 def lookups(self, request, model_admin):
     return [('filial', 'Указан филиал'),('nofilial', 'Не указан филиал'),]

 def queryset(self, request, queryset):
     if self.value() == 'filial':
         return queryset.filter(filial__isnull=False)
     elif self.value() == 'nofilial':
         return queryset.filter(filial__isnull=True)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    actions = ['set_draft', 'set_published']
    fields = ('title', 'slug', 'content', 'photo', 'cat', 'filial', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'time_create', 'is_published', 'post_photo', 'cat', 'days_since_publication')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    ordering = ['-time_create', 'title']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [FilialFilter, 'cat__name', 'is_published']

    @admin.display(description="Изображение")
    def post_photo(self, post: Post):
        if post.photo:
            return mark_safe(f"<img src = '{post.photo.url}'width = 50 > ")
        return "Без фото"

    @admin.display(description="Дней с публикации")
    def days_since_publication(self, post: Post):
        if post.time_create:
            delta = date.today() - post.time_create.date()
            return f"{delta.days} дн."
        return "Нет даты"

    @admin.action(description="Снять с публикации выбранные записи")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Post.Status.DRAFT)
        self.message_user(request, f"Снято с публикации {count} записи(ей)")

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей)")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
 list_display = ('id', 'name')
 list_display_links = ('id', 'name')