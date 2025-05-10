from django.urls import path, include
from .views import cv_list_view, cv_detail_view, download_cv_pdf, send_cv_pdf_view

urlpatterns = [
    path('', cv_list_view, name='cv-list'),
    path('cv/<int:pk>/', cv_detail_view, name='cv_detail'),
    path('cv/<int:pk>/download/', download_cv_pdf, name='cv-pdf'),
    path('cv/<int:pk>/send_pdf/', send_cv_pdf_view, name='send-cv-pdf'),
    path('api/', include('main.api_urls')),
]
