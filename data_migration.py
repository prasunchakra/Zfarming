#!/usr/bin/env python
"""
Script to migrate data from the original CSV to Django models.
Run this after setting up the Django project.
"""

import os
import sys
import django
import pandas as pd
from pathlib import Path

# Setup Django
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zfarming.settings')
django.setup()

from apps.plants.models import Plant, PlantCategory, PlantCareGuide


def create_categories():
    """Create plant categories."""
    categories = [
        {'name': 'Herbs', 'description': 'Culinary and aromatic herbs perfect for cooking'},
        {'name': 'Flowers', 'description': 'Beautiful flowering plants for decoration'},
        {'name': 'Vegetables', 'description': 'Edible vegetables you can grow at home'},
        {'name': 'Succulents', 'description': 'Low-maintenance plants that store water'},
        {'name': 'Air Purifying', 'description': 'Plants that help clean indoor air'},
    ]
    
    for cat_data in categories:
        category, created = PlantCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"Created category: {category.name}")


def migrate_plant_data():
    """Migrate plant data from CSV to Django models."""
    # Path to the original CSV file
    csv_path = BASE_DIR / 'data' / 'plants.csv'
    
    if not csv_path.exists():
        print(f"CSV file not found at {csv_path}")
        return
    
    # Read CSV data
    df = pd.read_csv(csv_path)
    
    # Category mapping
    category_mapping = {
        'mint': ['Herbs'],
        'basil': ['Herbs'],
        'parsley': ['Herbs'],
        'cilantro': ['Herbs'],
        'rosemary': ['Herbs'],
        'lavender': ['Herbs'],
        'marigold': ['Flowers'],
        'peace_lily': ['Flowers', 'Air Purifying'],
        'snake_plant': ['Succulents', 'Air Purifying'],
        'spider_plant': ['Air Purifying'],
        'aloe_vera': ['Succulents'],
        'cherry_tomatoes': ['Vegetables'],
        'chilli': ['Vegetables'],
        'lettuce': ['Vegetables'],
    }
    
    for _, row in df.iterrows():
        # Create or update plant
        plant, created = Plant.objects.get_or_create(
            plant_id=row['plant_id'],
            defaults={
                'name': row['name'],
                'scientific_name': row['scientific_name'],
                'sunlight': row['sunlight'],
                'space': row['space'],
                'care_level': row['care_level'],
                'image_url': row['image_url'],
                'tagline': row['tagline'],
                'description': row['description'],
                'watering_frequency': row['watering_frequency'],
                'pot_size': row['pot_size'],
                'sunlight_needs': row['sunlight_needs'],
                'watering_guide': row['watering_guide'],
                'sunlight_guide': row['sunlight_guide'],
                'potting_tips': row['potting_tips'],
                'common_issues': row['common_issues'],
                'is_beginner_friendly': 'Beginner' in row['care_level'],
                'is_featured': True,  # Mark all initial plants as featured
            }
        )
        
        # Add categories
        if row['plant_id'] in category_mapping:
            for cat_name in category_mapping[row['plant_id']]:
                try:
                    category = PlantCategory.objects.get(name=cat_name)
                    plant.categories.add(category)
                except PlantCategory.DoesNotExist:
                    print(f"Category {cat_name} not found for {plant.name}")
        
        # Create care guide
        care_guide, guide_created = PlantCareGuide.objects.get_or_create(
            plant=plant,
            defaults={
                'fertilizing_guide': f"Fertilize {plant.name} monthly during growing season (spring/summer)",
                'pruning_guide': f"Prune {plant.name} as needed to maintain shape and remove dead growth",
                'repotting_guide': f"Repot {plant.name} every 1-2 years or when rootbound",
                'pest_control': "Watch for common pests like aphids and spider mites. Use insecticidal soap if needed.",
                'disease_prevention': "Ensure good air circulation and avoid overwatering to prevent fungal issues.",
                'pro_tips': f"Best grown in {row['space'].lower()}. {row['common_issues']}",
                'common_mistakes': "Overwatering is the most common mistake. Let soil dry between waterings.",
            }
        )
        
        if created:
            print(f"Created plant: {plant.name}")
        if guide_created:
            print(f"Created care guide for: {plant.name}")


def main():
    """Main migration function."""
    print("Starting data migration...")
    
    # Create categories first
    create_categories()
    
    # Migrate plant data
    migrate_plant_data()
    
    print("Data migration completed!")
    print(f"Total plants: {Plant.objects.count()}")
    print(f"Total categories: {PlantCategory.objects.count()}")
    print(f"Total care guides: {PlantCareGuide.objects.count()}")


if __name__ == '__main__':
    main()
