from django.urls import path, register_converter, include
from cocoa import views, converters
from django.contrib import admin

# ✅ Импорт для медиа-файлов:
from django.conf import settings
from django.conf.urls.static import static

from cocoahouse import settings

admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Кафе, специализированное на какао COCOAHOUSE"

register_converter(converters.MonthConverter, "month")

urlpatterns = [
    path('', views.CocoaHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('seasons/', views.seasons, name='seasons'),
    path('login/', views.login, name='login'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('category/<slug:cat_slug>/',views.CocoaCategory.as_view(), name='category'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('addpage/', views.AddPage.as_view(), name='addpage'),
    path('edit/<int:pk>/', views.UpdatePage.as_view(),name='edit_page'),
    path('edit/<slug:slug>/', views.UpdatePage.as_view(),name='edit_page'),
    path('delete/<int:pk>', views.DeletePage.as_view(), name='delete_post'),


    path('cacao/', views.category_cacao, name='category_cacao'),
    path('hot-drinks/', views.category_hot_drinks, name='category_hot_drinks'),
    path('cold-drinks/', views.category_cold_drinks, name='category_cold_drinks'),
    path('baking/', views.category_baking, name='category_baking'),
    path('desserts/', views.category_desserts, name='category_desserts'),
    path('merch/', views.category_merch, name='category_merch'),
    path('gift-sets/', views.category_gift_sets, name='category_gift_sets'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
