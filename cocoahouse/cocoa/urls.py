from django.urls import path, register_converter
from cocoa import views, converters

register_converter(converters.MonthConverter, "month")

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('catalog/', views.catalog, name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('seasons/', views.seasons, name='seasons'),
    path('login/', views.login, name='login'),
    path('tag/<slug:tag_slug>/', views.show_tag_postlist, name='tag'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('category/<slug:cat_slug>/', views.show_category,name='category'),


    path('cacao/', views.category_cacao, name='category_cacao'),
    path('hot-drinks/', views.category_hot_drinks, name='category_hot_drinks'),
    path('cold-drinks/', views.category_cold_drinks, name='category_cold_drinks'),
    path('baking/', views.category_baking, name='category_baking'),
    path('desserts/', views.category_desserts, name='category_desserts'),
    path('merch/', views.category_merch, name='category_merch'),
    path('gift-sets/', views.category_gift_sets, name='category_gift_sets'),
]

