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
    template_name = 'core/home_simple.html'


class AboutView(TemplateView):
    """
    About page with application information.
    """
    template_name = 'core/about.html'
