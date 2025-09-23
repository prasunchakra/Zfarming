"""
API views for the ZFarming application.
"""
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Q
from apps.plants.models import Plant, PlantCategory


class PlantViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for plants.
    """
    queryset = Plant.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        queryset = Plant.objects.filter(is_active=True)
        
        # Search functionality
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(scientific_name__icontains=search)
            )
        
        # Filter by care level
        care_level = self.request.query_params.get('care_level')
        if care_level:
            queryset = queryset.filter(care_level__icontains=care_level)
        
        return queryset


class PlantCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API viewset for plant categories.
    """
    queryset = PlantCategory.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class PlantIdentificationAPIView(APIView):
    """
    API endpoint for plant identification.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        # This would integrate with the PlantIdentificationService
        return Response({
            'message': 'Plant identification API endpoint',
            'status': 'coming_soon'
        })


class PlantRecommendationAPIView(APIView):
    """
    API endpoint for plant recommendations.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request):
        sunlight = request.data.get('sunlight')
        space = request.data.get('space')
        care_level = request.data.get('care_level')
        
        plants = Plant.objects.filter(
            sunlight=sunlight,
            space=space,
            care_level=care_level,
            is_active=True
        )[:6]
        
        # Return basic plant data
        results = []
        for plant in plants:
            results.append({
                'id': plant.id,
                'name': plant.name,
                'scientific_name': plant.scientific_name,
                'tagline': plant.tagline,
                'image_url': plant.primary_image,
                'care_level': plant.care_level_display,
                'sunlight': plant.sunlight_display,
                'space': plant.space_display,
            })
        
        return Response({
            'plants': results,
            'count': len(results)
        })
