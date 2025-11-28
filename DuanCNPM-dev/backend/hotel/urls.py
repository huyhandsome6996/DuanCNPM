from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('manager/', views.dashboard_manager, name='dashboard_manager'),
    path('employee/', views.dashboard_employee, name='dashboard_employee'),

    # Khách hàng
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('customers/<int:makhachhang>/edit/', views.customer_update, name='customer_update'),
    path('customers/<int:makhachhang>/delete/', views.customer_delete, name='customer_delete'),

    # Phòng
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('rooms/<str:maphong>/edit/', views.room_update, name='room_update'),
    path('rooms/<str:maphong>/delete/', views.room_delete, name='room_delete'),

    # Đặt phòng
    path('bookings/', views.booking_list, name='booking_list'),     # 👈 mới thêm
    path('bookings/add/', views.booking_create, name='booking_create'),
    
    # API chat AI nếu có
    # path('api/chat/', views.chat_ai, name='chat_ai'),
]
