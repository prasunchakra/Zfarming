"""
Models for the plants app.
"""
from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify


class PlantCategory(models.Model):
    """
    Categories for plants (Herbs, Flowers, Vegetables, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Plant Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Plant(models.Model):
    """
    Main plant model based on the CSV data structure.
    """
    SUNLIGHT_CHOICES = [
        ('Low Light (No direct sun)', 'Low Light (No direct sun)'),
        ('Medium Light (A few hours)', 'Medium Light (A few hours)'),
        ('Bright Light (6+ hours)', 'Bright Light (6+ hours)'),
    ]
    
    SPACE_CHOICES = [
        ('Small Pot (Windowsill)', 'Small Pot (Windowsill)'),
        ('Hanging Basket', 'Hanging Basket'),
        ('Medium Container', 'Medium Container'),
        ('Large Container (Balcony)', 'Large Container (Balcony)'),
    ]
    
    CARE_LEVEL_CHOICES = [
        ('Beginner (I forget to water)', 'Beginner (I forget to water)'),
        ('Intermediate (I can follow a schedule)', 'Intermediate (I can follow a schedule)'),
        ('Advanced (I love plant care)', 'Advanced (I love plant care)'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    plant_id = models.CharField(max_length=100, unique=True, help_text="Unique identifier for API")
    
    # Categories and Tags
    categories = models.ManyToManyField(PlantCategory, blank=True)
    
    # Care Requirements
    sunlight = models.CharField(max_length=50, choices=SUNLIGHT_CHOICES)
    space = models.CharField(max_length=50, choices=SPACE_CHOICES)
    care_level = models.CharField(max_length=50, choices=CARE_LEVEL_CHOICES)
    
    # Images and Visual
    image_url = models.URLField(blank=True, help_text="External image URL")
    image = models.ImageField(upload_to='plants/', blank=True, help_text="Upload local image")
    
    # Descriptions
    tagline = models.CharField(max_length=200, help_text="Short catchy description")
    description = models.TextField(help_text="Detailed description")
    
    # Care Details
    watering_frequency = models.CharField(max_length=100)
    pot_size = models.CharField(max_length=100)
    sunlight_needs = models.TextField()
    watering_guide = models.TextField()
    sunlight_guide = models.TextField()
    potting_tips = models.TextField()
    common_issues = models.TextField()
    
    # Metadata
    is_featured = models.BooleanField(default=False)
    is_beginner_friendly = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['plant_id']),
            models.Index(fields=['sunlight', 'care_level']),
            models.Index(fields=['is_featured', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.scientific_name})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.scientific_name}")
        if not self.meta_description:
            self.meta_description = f"{self.tagline} Learn how to care for {self.name}."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('plants:detail', kwargs={'slug': self.slug})
    
    @property
    def primary_image(self):
        """Return the primary image (uploaded image first, then URL)"""
        if self.image:
            return self.image.url
        return self.image_url
    
    @property
    def care_level_display(self):
        """Get a clean care level display"""
        return self.care_level.split('(')[0].strip()
    
    @property
    def sunlight_display(self):
        """Get a clean sunlight display"""
        return self.sunlight.split('(')[0].strip()
    
    @property
    def space_display(self):
        """Get a clean space display"""
        return self.space.split('(')[0].strip()


class PlantCareGuide(models.Model):
    """
    Extended care guides for plants.
    """
    plant = models.OneToOneField(Plant, on_delete=models.CASCADE, related_name='care_guide')
    
    # Monthly care calendar
    january_care = models.TextField(blank=True)
    february_care = models.TextField(blank=True)
    march_care = models.TextField(blank=True)
    april_care = models.TextField(blank=True)
    may_care = models.TextField(blank=True)
    june_care = models.TextField(blank=True)
    july_care = models.TextField(blank=True)
    august_care = models.TextField(blank=True)
    september_care = models.TextField(blank=True)
    october_care = models.TextField(blank=True)
    november_care = models.TextField(blank=True)
    december_care = models.TextField(blank=True)
    
    # Additional care information
    fertilizing_guide = models.TextField(blank=True)
    pruning_guide = models.TextField(blank=True)
    repotting_guide = models.TextField(blank=True)
    pest_control = models.TextField(blank=True)
    disease_prevention = models.TextField(blank=True)
    
    # Tips and tricks
    pro_tips = models.TextField(blank=True)
    common_mistakes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Care Guide for {self.plant.name}"


class PlantImage(models.Model):
    """
    Additional images for plants.
    """
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='additional_images')
    image = models.ImageField(upload_to='plants/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"{self.plant.name} - Image {self.id}"
