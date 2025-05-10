from django.contrib import admin
from django.urls import path, include

from CVProject.views import settings_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', settings_view, name='settings_page'),
    path('', include('main.urls')),
    path('', include('audit.urls')),
]
