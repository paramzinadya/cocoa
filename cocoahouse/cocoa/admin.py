from django.contrib import admin
from .models import Post, Category

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
    actions = ['set_published']
    fields = ('title', 'slug', 'content', 'cat', 'filial', 'is_published')
    prepopulated_fields = {"slug": ("title",)}
    list_display = ('title', 'time_create', 'is_published', 'cat', 'brief_info')
    list_display_links = ('title', )
    list_editable = ('is_published', )
    ordering = ['-time_create', 'title']
    search_fields = ['title__startswith', 'cat__name']
    list_filter = [FilialFilter, 'cat__name', 'is_published']

    @admin.display(description="Краткое описание")
    def brief_info(self, post: Post):
        return f"Описание {len(post.content)} символов."

    @admin.action(description="Опубликовать выбранные записи")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Post.Status.PUBLISHED)
        self.message_user(request, f"Изменено {count} записи(ей)")

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
 list_display = ('id', 'name')
 list_display_links = ('id', 'name')



