"""
Views for the plants app.
"""
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Plant, PlantCategory


class PlantListView(ListView):
    """
    List view for all plants with search and filtering.
    """
    model = Plant
    template_name = 'plants/list.html'
    context_object_name = 'plants'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Plant.objects.filter(is_active=True).select_related().prefetch_related('categories')
        
        # Search functionality
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(scientific_name__icontains=search) |
                Q(tagline__icontains=search)
            )
        
        # Filter by care level
        care_level = self.request.GET.get('care_level')
        if care_level:
            queryset = queryset.filter(care_level__icontains=care_level)
        
        # Filter by sunlight
        sunlight = self.request.GET.get('sunlight')
        if sunlight:
            queryset = queryset.filter(sunlight=sunlight)
        
        return queryset.order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = PlantCategory.objects.all()
        context['sunlight_choices'] = Plant.SUNLIGHT_CHOICES
        context['care_level_choices'] = Plant.CARE_LEVEL_CHOICES
        return context


class PlantDetailView(DetailView):
    """
    Detail view for individual plants.
    """
    model = Plant
    template_name = 'plants/detail.html'
    context_object_name = 'plant'
    slug_field = 'slug'
    
    def get_queryset(self):
        return Plant.objects.filter(is_active=True).select_related('care_guide').prefetch_related('categories', 'additional_images')


class PlantCategoryView(ListView):
    """
    List plants by category.
    """
    model = Plant
    template_name = 'plants/category.html'
    context_object_name = 'plants'
    paginate_by = 12
    
    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Plant.objects.filter(
            categories__slug=category_slug,
            is_active=True
        ).distinct().order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs['slug']
        try:
            context['category'] = PlantCategory.objects.get(slug=category_slug)
        except PlantCategory.DoesNotExist:
            context['category'] = None
        return context
