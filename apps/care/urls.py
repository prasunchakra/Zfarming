"""
URLs for the care app.
"""
from django.urls import path
from . import views

app_name = 'care'

urlpatterns = [
    path('', views.CareHubView.as_view(), name='hub'),
    path('<slug:slug>/', views.PlantCareDetailView.as_view(), name='detail'),
]
