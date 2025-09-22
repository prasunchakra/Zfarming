"""
URLs for the API app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'plants', views.PlantViewSet)
router.register(r'categories', views.PlantCategoryViewSet)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('scanner/identify/', views.PlantIdentificationAPIView.as_view(), name='identify'),
    path('finder/recommend/', views.PlantRecommendationAPIView.as_view(), name='recommend'),
]
