from django.urls import path
from . import views

urlpatterns = [
    path('revenue/', views.revenue_report, name='revenue'),
    path('customers/', views.customer_report, name='customers'),
]
