from django.urls import path
from . import views

app_name = 'quanly'
urlpatterns = [
    path('', views.trang_chu, name='trang_chu'),
    path('phong/', views.danh_sach_phong, name='danh_sach_phong'),
    path('phong/<int:pk>/', views.chi_tiet_phong, name='chi_tiet_phong'),
    path('dich-vu/', views.danh_sach_dich_vu, name='danh_sach_dich_vu'),
    path('dat-phong/', views.dat_phong, name='dat_phong'),
    path('dat-phong/<int:pk>/chi-tiet/', views.chi_tiet_datphong, name='chi_tiet_datphong'),
    path('dat-phong/<int:datphong_id>/them-phong/', views.them_chi_tiet_datphong, name='them_chi_tiet_datphong'),
    path('dat-phong/<int:datphong_id>/checkin/', views.checkin_view, name='checkin'),
    path('dat-phong/<int:datphong_id>/checkout/', views.checkout_view, name='checkout'),
    path('hoa-don/tao/<int:pk>/', views.tao_hoa_don, name='tao_hoa_don'),  # implement view tao_hoa_don nếu cần
    path('call-sp/', views.call_proc_example, name='call_proc_example'),
]
