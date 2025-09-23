"""
URLs for the plants app.
"""
from django.urls import path
from . import views

app_name = 'plants'

urlpatterns = [
    path('', views.PlantListView.as_view(), name='list'),
    path('<slug:slug>/', views.PlantDetailView.as_view(), name='detail'),
    path('category/<slug:slug>/', views.PlantCategoryView.as_view(), name='category'),
]
