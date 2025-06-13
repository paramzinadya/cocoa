main_menu = [{'title': "О сайте", 'url_name': 'about'},
 {'title': "Каталог", 'url_name': 'catalog'},
 {'title': "Обратная связь", 'url_name': 'contact'},
 {'title': "Добавить пост", 'url_name': 'addpage'}
]

class DataMixin:
    title_page = None
    extra_context = {}
    paginate_by = 2

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        #if 'main_menu' not in self.extra_context:
            #self.extra_context['main_menu'] = main_menu

    def get_mixin_context(self, context, **kwargs):
        if self.title_page:
            context['title'] = self.title_page
        #context['main_menu'] = main_menu
        context['cat_selected'] = None
        context.update(kwargs)
        return context
