from django.urls import path

from show_app import views
from show_app.ajax import search_view, subscribe_view

urlpatterns = [
    path('sitemap.xml/', views.sitemap),
    path('', views.index, name='index'),
    path('show/<int:pk>/subscribe_ajax/', subscribe_view),
    path('show/<int:pk>/search/', search_view),
    path('about/', views.about_view, name='about'),
    path('anime/', views.index, name='anime'),
    path('shows/', views.index, name='shows'),
    path('show/<int:pk>/', views.detail_show, name='show'),
    path('cartoons/', views.index, name='cartoons'),
    path('search/', search_view),
    path('<str:show_type>/search/', search_view),
    path('telegram/', views.telegram_view)

]
