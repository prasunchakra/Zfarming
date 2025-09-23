"""
User models for the accounts app.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.plants.models import Plant


class User(AbstractUser):
    """
    Custom user model with gardening preferences.
    """
    EXPERIENCE_CHOICES = [
        ('beginner', 'Complete Beginner'),
        ('some_experience', 'Some Experience'),
        ('experienced', 'Experienced Gardener'),
    ]
    
    SPACE_CHOICES = [
        ('windowsill', 'Windowsill Only'),
        ('small_balcony', 'Small Balcony'),
        ('large_balcony', 'Large Balcony'),
        ('garden', 'Garden/Yard'),
        ('indoor_only', 'Indoor Only'),
    ]
    
    # Profile information
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    
    # Gardening preferences
    experience_level = models.CharField(
        max_length=20, 
        choices=EXPERIENCE_CHOICES, 
        blank=True
    )
    available_space = models.CharField(
        max_length=20, 
        choices=SPACE_CHOICES, 
        blank=True
    )
    sunlight_hours = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Hours of direct sunlight available"
    )
    preferred_care_level = models.CharField(
        max_length=50,
        choices=Plant.CARE_LEVEL_CHOICES,
        blank=True
    )
    
    # Preferences
    favorite_plants = models.ManyToManyField(Plant, blank=True, related_name='favorited_by')
    newsletter_subscription = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.email})"
    
    @property
    def has_complete_profile(self):
        """Check if user has completed their gardening profile"""
        return all([
            self.experience_level,
            self.available_space,
            self.sunlight_hours is not None,
            self.preferred_care_level,
        ])


class UserPlantCollection(models.Model):
    """
    Track plants that users own or want to grow.
    """
    STATUS_CHOICES = [
        ('want_to_grow', 'Want to Grow'),
        ('currently_growing', 'Currently Growing'),
        ('successfully_grown', 'Successfully Grown'),
        ('had_issues', 'Had Issues With'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plant_collection')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, help_text="Personal notes about this plant")
    date_added = models.DateTimeField(auto_now_add=True)
    date_planted = models.DateField(null=True, blank=True)
    
    # Care tracking
    last_watered = models.DateField(null=True, blank=True)
    last_fertilized = models.DateField(null=True, blank=True)
    last_repotted = models.DateField(null=True, blank=True)
    
    # Success metrics
    rating = models.PositiveIntegerField(
        null=True, 
        blank=True, 
        help_text="Rate this plant (1-5 stars)"
    )
    would_recommend = models.BooleanField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['user', 'plant']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.plant.name} ({self.status})"


class PlantIdentificationHistory(models.Model):
    """
    Track plant identification attempts by users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='identification_history')
    image = models.ImageField(upload_to='identifications/')
    
    # Results
    identified_plant = models.ForeignKey(
        Plant, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        help_text="Plant that was identified (if any)"
    )
    api_response = models.JSONField(help_text="Full API response for debugging")
    confidence_score = models.FloatField(null=True, blank=True)
    
    # User feedback
    user_confirmed = models.BooleanField(null=True, blank=True)
    user_feedback = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Plant Identification History"
    
    def __str__(self):
        plant_name = self.identified_plant.name if self.identified_plant else "Unknown"
        return f"{self.user.username} - {plant_name} ({self.created_at.date()})"
