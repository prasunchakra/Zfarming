"""
Views for the finder app.
"""
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from apps.plants.models import Plant


class PlantFinderForm(forms.Form):
    """
    Form for plant finder preferences.
    """
    sunlight = forms.ChoiceField(
        choices=Plant.SUNLIGHT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    space = forms.ChoiceField(
        choices=Plant.SPACE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    care_level = forms.ChoiceField(
        choices=Plant.CARE_LEVEL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class PlantFinderView(FormView):
    """
    Plant finder page - equivalent to Streamlit finder page.
    """
    template_name = 'finder/find.html'
    form_class = PlantFinderForm
    success_url = '/finder/results/'
    
    def form_valid(self, form):
        # Store form data in session for results page
        self.request.session['finder_preferences'] = form.cleaned_data
        return super().form_valid(form)


class PlantRecommendationsView(TemplateView):
    """
    Display plant recommendations based on user preferences.
    """
    template_name = 'finder/results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get preferences from session
        preferences = self.request.session.get('finder_preferences', {})
        
        if preferences:
            # Filter plants based on preferences
            plants = Plant.objects.filter(
                sunlight=preferences.get('sunlight'),
                space=preferences.get('space'),
                care_level=preferences.get('care_level'),
                is_active=True
            )[:6]  # Limit to 6 results
            
            # If no exact matches, show similar plants
            if not plants:
                plants = Plant.objects.filter(
                    care_level=preferences.get('care_level'),
                    is_active=True
                )[:6]
            
            context['plants'] = plants
            context['preferences'] = preferences
        
        return context
