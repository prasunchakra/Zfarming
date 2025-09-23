"""
Plant identification services.
"""
import base64
import requests
import logging
from typing import List, Dict, Optional
from django.conf import settings
from apps.plants.models import Plant

logger = logging.getLogger(__name__)


class PlantIdentificationService:
    """
    Service for identifying plants using external APIs.
    """
    
    def __init__(self):
        self.api_key = settings.PLANT_ID_API_KEY
        self.api_url = settings.PLANT_ID_API_URL
    
    def identify_plant(self, image_file) -> List[Dict]:
        """
        Identify a plant from an image file.
        
        Args:
            image_file: Django UploadedFile object
            
        Returns:
            List of identification results with confidence scores
        """
        if not self.api_key:
            logger.warning("Plant ID API key not configured, using mock data")
            return self._get_mock_results()
        
        try:
            # Convert image to base64
            image_data = image_file.read()
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Prepare API request
            headers = {
                "Api-Key": self.api_key,
                "Content-Type": "application/json"
            }
            
            payload = {
                "images": [image_base64],
                "modifiers": ["crops_fast", "similar_images"],
                "plant_details": [
                    "common_names", 
                    "url", 
                    "name_authority", 
                    "wiki_description", 
                    "taxonomy", 
                    "synonyms"
                ]
            }
            
            # Make API request
            response = requests.post(
                self.api_url, 
                headers=headers, 
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            # Process response
            data = response.json()
            return self._process_api_response(data)
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Plant ID API request failed: {e}")
            return self._get_mock_results()
        except Exception as e:
            logger.error(f"Plant identification error: {e}")
            return []
    
    def _process_api_response(self, data: Dict) -> List[Dict]:
        """
        Process the Plant.id API response into our format.
        """
        results = []
        suggestions = data.get('suggestions', [])
        
        for suggestion in suggestions[:5]:  # Top 5 results
            plant_name = suggestion.get('plant_name', 'Unknown')
            probability = suggestion.get('probability', 0.0)
            
            # Try to find matching plant in our database
            matched_plant = self._find_matching_plant(plant_name, suggestion)
            
            result = {
                'plant_name': plant_name,
                'common_name': self._extract_common_name(plant_name),
                'scientific_name': self._extract_scientific_name(suggestion),
                'confidence': probability,
                'matched_plant': matched_plant,
                'plant_id': matched_plant.plant_id if matched_plant else None,
                'api_data': suggestion  # Store full API response
            }
            results.append(result)
        
        return results
    
    def _find_matching_plant(self, plant_name: str, suggestion: Dict) -> Optional[Plant]:
        """
        Try to find a matching plant in our database.
        """
        # Extract possible names to search for
        search_terms = [plant_name]
        
        # Add common names from API
        common_names = suggestion.get('plant_details', {}).get('common_names', [])
        search_terms.extend(common_names)
        
        # Add scientific name
        scientific_name = self._extract_scientific_name(suggestion)
        if scientific_name:
            search_terms.append(scientific_name)
        
        # Search our database
        for term in search_terms:
            if not term:
                continue
                
            # Try exact name match
            plant = Plant.objects.filter(
                name__iexact=term,
                is_active=True
            ).first()
            if plant:
                return plant
            
            # Try scientific name match
            plant = Plant.objects.filter(
                scientific_name__iexact=term,
                is_active=True
            ).first()
            if plant:
                return plant
            
            # Try partial name match
            plant = Plant.objects.filter(
                name__icontains=term,
                is_active=True
            ).first()
            if plant:
                return plant
        
        return None
    
    def _extract_common_name(self, plant_name: str) -> str:
        """Extract common name from plant name string."""
        # Plant.id often returns names like "Common Name (Scientific Name)"
        if '(' in plant_name:
            return plant_name.split('(')[0].strip()
        return plant_name
    
    def _extract_scientific_name(self, suggestion: Dict) -> str:
        """Extract scientific name from API suggestion."""
        plant_details = suggestion.get('plant_details', {})
        scientific_name = plant_details.get('structured_name', {}).get('species', '')
        
        if not scientific_name:
            # Try to extract from plant_name if it contains parentheses
            plant_name = suggestion.get('plant_name', '')
            if '(' in plant_name and ')' in plant_name:
                scientific_name = plant_name.split('(')[1].split(')')[0].strip()
        
        return scientific_name
    
    def _get_mock_results(self) -> List[Dict]:
        """
        Return mock results for development/demo purposes.
        """
        # Get some sample plants from our database
        sample_plants = Plant.objects.filter(is_active=True)[:3]
        
        mock_results = []
        confidences = [0.89, 0.76, 0.65]
        
        for i, plant in enumerate(sample_plants):
            if i >= len(confidences):
                break
                
            result = {
                'plant_name': f"{plant.name} ({plant.scientific_name})",
                'common_name': plant.name,
                'scientific_name': plant.scientific_name,
                'confidence': confidences[i],
                'matched_plant': plant,
                'plant_id': plant.plant_id,
                'api_data': {
                    'plant_name': plant.name,
                    'probability': confidences[i],
                    'plant_details': {
                        'common_names': [plant.name],
                    }
                }
            }
            mock_results.append(result)
        
        return mock_results
