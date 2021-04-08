from django.urls import path

from users.views import account_view, ajax_delete_show, trash_view, trash_clear

app_name = 'users'

urlpatterns = [
    path('<int:pk>/delete/', ajax_delete_show, name='delete'),
    path('<int:pk>/', account_view, name='account'),
    path('trash/<int:pk>/', trash_view, name='trash'),
    path('trash/clear/<int:pk>', trash_clear, name='trash_clear'),

]
