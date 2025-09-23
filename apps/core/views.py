"""
Views for the core app.
"""
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.plants.models import Plant


class HomeView(TemplateView):
    """
    Home page view - equivalent to the main Streamlit app.py
    """
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_plants'] = Plant.objects.filter(
            care_level__icontains='Beginner'
        )[:6]
        return context


class AboutView(TemplateView):
    """
    About page with application information.
    """
    template_name = 'core/about.html'
