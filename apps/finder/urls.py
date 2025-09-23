"""
URLs for the finder app.
"""
from django.urls import path
from . import views

app_name = 'finder'

urlpatterns = [
    path('', views.PlantFinderView.as_view(), name='find'),
    path('results/', views.PlantRecommendationsView.as_view(), name='results'),
]
