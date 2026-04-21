# core/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from dashboard.views import home_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('', home_redirect, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)