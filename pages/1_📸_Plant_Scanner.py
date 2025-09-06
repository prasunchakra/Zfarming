import streamlit as st
import requests
import base64
import json
from PIL import Image
import io

# Configure the page
st.set_page_config(
    page_title="Plant Scanner - Zfarming",
    page_icon="📸",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #2E8B57;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
        font-style: italic;
    }
    
    .plant-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }
    
    .plant-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
</style>
""", unsafe_allow_html=True)

def identify_plant(image_file):
    """
    Identify plant using Plant.id API (free tier)
    For this POC, we'll simulate the API response with realistic plant data
    In production, you would integrate with Plant.id API or similar service
    """
    try:
        # For POC demonstration, we'll return simulated results
        # In production, uncomment the code below to use real API
        
        # Real API implementation (commented for POC):
        # return call_plant_id_api(image_file)
        
        # Simulated results for POC
        simulated_results = [
            {
                "plant_name": "Snake Plant (Sansevieria trifasciata)",
                "common_name": "Snake Plant",
                "confidence": 0.89,
                "scientific_name": "Sansevieria trifasciata",
                "plant_id": "snake_plant"
            },
            {
                "plant_name": "Spider Plant (Chlorophytum comosum)",
                "common_name": "Spider Plant", 
                "confidence": 0.76,
                "scientific_name": "Chlorophytum comosum",
                "plant_id": "spider_plant"
            },
            {
                "plant_name": "Peace Lily (Spathiphyllum wallisii)",
                "common_name": "Peace Lily",
                "confidence": 0.65,
                "scientific_name": "Spathiphyllum wallisii", 
                "plant_id": "peace_lily"
            }
        ]
        
        return simulated_results
        
    except Exception as e:
        st.error(f"Error identifying plant: {str(e)}")
        return []

def display_results(results):
    """Display plant identification results"""
    if not results:
        st.warning("No plants identified. Please try with a clearer image of a plant leaf.")
        return
    
    st.markdown("### 🌿 Identification Results")
    st.markdown("Here are the most likely matches for your plant:")
    
    for i, result in enumerate(results[:3]):  # Show top 3 results
        with st.container():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{i+1}. {result['plant_name']}**")
                st.markdown(f"*{result['scientific_name']}*")
                
            with col2:
                confidence_percent = int(result['confidence'] * 100)
                st.metric("Confidence", f"{confidence_percent}%")
            
            # Confidence bar
            confidence_bar = result['confidence']
            st.progress(confidence_bar)
            
            # Link to plant care guide
            if st.button(f"📖 View Care Guide for {result['common_name']}", 
                       key=f"guide_{i}", 
                       help="Click to see detailed care instructions"):
                # In a real app, this would navigate to the specific plant's care guide
                st.session_state['selected_plant'] = result['plant_id']
                st.success(f"🎉 Great choice! {result['common_name']} is an excellent plant for beginners.")
                st.info("💡 Tip: Use the Plant Care Hub to find detailed care instructions for this plant.")
            
            st.markdown("---")
    
    # Additional tips
    st.markdown("### 💡 Tips for Better Identification")
    st.markdown("""
    - Take photos in good lighting
    - Focus on individual leaves rather than the whole plant
    - Make sure the leaf is clearly visible and not blurry
    - Try different angles if the first attempt doesn't work well
    """)

def call_plant_id_api(image_file):
    """
    Real implementation for Plant.id API
    This would be used in production
    """
    # API endpoint
    url = "https://api.plant.id/v3/identification"
    
    # API key (you would store this in environment variables)
    api_key = "YOUR_API_KEY_HERE"
    
    # Prepare headers
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    # Convert image to base64
    image_bytes = image_file.read()
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    # Prepare request data
    data = {
        "images": [image_base64],
        "modifiers": ["crops_fast", "similar_images"],
        "plant_details": ["common_names", "url", "name_authority", "wiki_description", "taxonomy", "synonyms"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Main content
st.markdown('<h1 class="main-header">📸 Plant Scanner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Identify any plant instantly! Take a photo or upload an image of any plant leaf.</p>', unsafe_allow_html=True)

# Image input section
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("### 📷 Take a Photo")
    camera_image = st.camera_input("Point your camera at a plant leaf")
    
with col2:
    st.markdown("### 📁 Upload Image")
    uploaded_file = st.file_uploader(
        "Or upload an existing image",
        type=['png', 'jpg', 'jpeg'],
        help="Upload a clear image of a plant leaf for best results"
    )

# Process the image
image_to_process = None
if camera_image is not None:
    image_to_process = camera_image
elif uploaded_file is not None:
    image_to_process = uploaded_file

if image_to_process is not None:
    # Display the uploaded image
    st.markdown("### 📸 Your Image")
    st.image(image_to_process, caption="Image to be analyzed", use_container_width=True)
    
    # Process button
    if st.button("🔍 Identify This Plant", type="primary", use_container_width=True):
        with st.spinner("Analyzing your plant... This may take a few seconds."):
            results = identify_plant(image_to_process)
            display_results(results)
