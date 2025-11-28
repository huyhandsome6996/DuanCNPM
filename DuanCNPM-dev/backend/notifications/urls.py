from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notification_list, name='list'),
    path('<int:id>/', views.notification_detail, name='detail'),
    path('create/', views.notification_create, name='create'),
]
