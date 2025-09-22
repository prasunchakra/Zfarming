"""
Admin configuration for the plants app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import PlantCategory, Plant, PlantCareGuide, PlantImage


@admin.register(PlantCategory)
class PlantCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


class PlantImageInline(admin.TabularInline):
    model = PlantImage
    extra = 1
    fields = ['image', 'caption', 'is_primary', 'order']


class PlantCareGuideInline(admin.StackedInline):
    model = PlantCareGuide
    extra = 0


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'scientific_name', 'care_level_display', 
        'sunlight_display', 'is_featured', 'is_active', 'image_preview'
    ]
    list_filter = [
        'care_level', 'sunlight', 'space', 'is_featured', 
        'is_active', 'categories', 'created_at'
    ]
    search_fields = ['name', 'scientific_name', 'plant_id', 'tagline']
    prepopulated_fields = {'slug': ('name', 'scientific_name')}
    filter_horizontal = ['categories']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'scientific_name', 'slug', 'plant_id')
        }),
        ('Images', {
            'fields': ('image', 'image_url')
        }),
        ('Care Requirements', {
            'fields': ('sunlight', 'space', 'care_level', 'categories')
        }),
        ('Descriptions', {
            'fields': ('tagline', 'description')
        }),
        ('Care Details', {
            'fields': (
                'watering_frequency', 'pot_size', 'sunlight_needs',
                'watering_guide', 'sunlight_guide', 'potting_tips', 'common_issues'
            )
        }),
        ('Settings', {
            'fields': ('is_featured', 'is_beginner_friendly', 'is_active')
        }),
        ('SEO', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [PlantCareGuideInline, PlantImageInline]
    
    def image_preview(self, obj):
        if obj.primary_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.primary_image
            )
        return "No image"
    image_preview.short_description = "Image"
    
    def care_level_display(self, obj):
        return obj.care_level_display
    care_level_display.short_description = "Care Level"
    
    def sunlight_display(self, obj):
        return obj.sunlight_display
    sunlight_display.short_description = "Sunlight"
    
    actions = ['make_featured', 'remove_featured', 'activate', 'deactivate']
    
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f"{queryset.count()} plants marked as featured.")
    make_featured.short_description = "Mark selected plants as featured"
    
    def remove_featured(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f"{queryset.count()} plants removed from featured.")
    remove_featured.short_description = "Remove selected plants from featured"
    
    def activate(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, f"{queryset.count()} plants activated.")
    activate.short_description = "Activate selected plants"
    
    def deactivate(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, f"{queryset.count()} plants deactivated.")
    deactivate.short_description = "Deactivate selected plants"


@admin.register(PlantCareGuide)
class PlantCareGuideAdmin(admin.ModelAdmin):
    list_display = ['plant', 'created_at', 'updated_at']
    search_fields = ['plant__name', 'plant__scientific_name']
    list_filter = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Plant', {
            'fields': ('plant',)
        }),
        ('Monthly Care Calendar', {
            'fields': (
                'january_care', 'february_care', 'march_care', 'april_care',
                'may_care', 'june_care', 'july_care', 'august_care',
                'september_care', 'october_care', 'november_care', 'december_care'
            ),
            'classes': ('collapse',)
        }),
        ('Additional Care Information', {
            'fields': (
                'fertilizing_guide', 'pruning_guide', 'repotting_guide',
                'pest_control', 'disease_prevention'
            )
        }),
        ('Tips and Tricks', {
            'fields': ('pro_tips', 'common_mistakes')
        })
    )


@admin.register(PlantImage)
class PlantImageAdmin(admin.ModelAdmin):
    list_display = ['plant', 'caption', 'is_primary', 'order', 'image_preview']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['plant__name', 'caption']
    list_editable = ['is_primary', 'order']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover;" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = "Preview"
