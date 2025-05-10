from django.urls import path, include
from .views import cv_list_view, cv_detail_view, download_cv_pdf

urlpatterns = [
    path('', cv_list_view, name='cv-list'),
    path('cv/<int:pk>/', cv_detail_view, name='cv-detail'),
    path('cv/<int:pk>/download/', download_cv_pdf, name='cv-pdf'),
    path('api/', include('main.api_urls')),
]
