# backend/backend/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('', include(('hotel.urls', 'hotel'), namespace='hotel')),  # trang chủ, dashboard
    path('hr/', include(('hr.urls', 'hr'), namespace='hr')),
    path('notifications/', include(('notifications.urls', 'notifications'), namespace='notifications')),
    path('reports/', include(('reports.urls', 'reports'), namespace='reports')),
]
