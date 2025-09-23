"""
URLs for the scanner app.
"""
from django.urls import path
from . import views

app_name = 'scanner'

urlpatterns = [
    path('', views.PlantScannerView.as_view(), name='scan'),
    path('identify/', views.PlantIdentificationView.as_view(), name='identify'),
    path('results/<int:pk>/', views.IdentificationResultView.as_view(), name='results'),
]
