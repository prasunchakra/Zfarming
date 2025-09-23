"""
Views for the care app.
"""
from django.views.generic import ListView, DetailView
from django.db.models import Q
from apps.plants.models import Plant


class CareHubView(ListView):
    """
    Care hub page - equivalent to Streamlit care hub page.
    """
    model = Plant
    template_name = 'care/hub.html'
    context_object_name = 'plants'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Plant.objects.filter(is_active=True).select_related('care_guide')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(scientific_name__icontains=search)
            )
        
        # Filter by care level
        care_level = self.request.GET.get('care_level')
        if care_level and care_level != 'All':
            queryset = queryset.filter(care_level__icontains=care_level)
        
        return queryset.order_by('name')


class PlantCareDetailView(DetailView):
    """
    Detailed plant care guide.
    """
    model = Plant
    template_name = 'care/detail.html'
    context_object_name = 'plant'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Plant.objects.filter(is_active=True).select_related('care_guide')
