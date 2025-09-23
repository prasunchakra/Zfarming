"""
Views for the scanner app.
"""
from django.views.generic import TemplateView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from .services import PlantIdentificationService
from apps.accounts.models import PlantIdentificationHistory


class PlantScannerView(TemplateView):
    """
    Plant scanner page - equivalent to Streamlit scanner page.
    """
    template_name = 'scanner/scan.html'


class PlantIdentificationView(LoginRequiredMixin, CreateView):
    """
    Handle plant identification from uploaded images.
    """
    model = PlantIdentificationHistory
    fields = ['image']
    template_name = 'scanner/identify.html'
    success_url = reverse_lazy('scanner:scan')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        
        # Get the uploaded image
        image_file = form.cleaned_data['image']
        
        # Identify the plant
        service = PlantIdentificationService()
        results = service.identify_plant(image_file)
        
        # Store the results
        if results:
            best_result = results[0]
            form.instance.api_response = {
                'results': results,
                'best_match': best_result
            }
            form.instance.confidence_score = best_result.get('confidence', 0.0)
            
            # Try to match with our plant database
            matched_plant = best_result.get('matched_plant')
            if matched_plant:
                form.instance.identified_plant = matched_plant
        
        response = super().form_valid(form)
        
        # Redirect to results page
        if self.object:
            return redirect('scanner:results', pk=self.object.pk)
        
        return response


class IdentificationResultView(LoginRequiredMixin, DetailView):
    """
    Display plant identification results.
    """
    model = PlantIdentificationHistory
    template_name = 'scanner/results.html'
    context_object_name = 'identification'
    
    def get_queryset(self):
        return PlantIdentificationHistory.objects.filter(user=self.request.user)
