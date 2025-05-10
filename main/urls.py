from django.urls import path
from .views import cv_list_view, cv_detail_view

urlpatterns = [
    path('', cv_list_view, name='cv-list'),
    path('cv/<int:pk>/', cv_detail_view, name='cv-detail'),

]
