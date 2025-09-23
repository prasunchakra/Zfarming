"""
Views for the accounts app.
"""
from django.views.generic import CreateView, TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth import login
from .models import User, UserPlantCollection, PlantIdentificationHistory


class RegisterView(CreateView):
    """
    User registration view.
    """
    model = User
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view.
    """
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['plant_count'] = UserPlantCollection.objects.filter(user=self.request.user).count()
        context['scan_count'] = PlantIdentificationHistory.objects.filter(user=self.request.user).count()
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """
    Edit user profile.
    """
    model = User
    fields = ['first_name', 'last_name', 'bio', 'experience_level', 'available_space', 'sunlight_hours', 'preferred_care_level']
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')
    
    def get_object(self):
        return self.request.user


class PlantCollectionView(LoginRequiredMixin, ListView):
    """
    User's plant collection.
    """
    model = UserPlantCollection
    template_name = 'accounts/collection.html'
    context_object_name = 'collection'
    
    def get_queryset(self):
        return UserPlantCollection.objects.filter(user=self.request.user).select_related('plant')


class IdentificationHistoryView(LoginRequiredMixin, ListView):
    """
    User's plant identification history.
    """
    model = PlantIdentificationHistory
    template_name = 'accounts/history.html'
    context_object_name = 'history'
    paginate_by = 10
    
    def get_queryset(self):
        return PlantIdentificationHistory.objects.filter(user=self.request.user).order_by('-created_at')
