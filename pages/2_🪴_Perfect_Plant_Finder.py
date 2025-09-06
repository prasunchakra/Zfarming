import streamlit as st
import pandas as pd
import os

# Configure the page
st.set_page_config(
    page_title="Perfect Plant Finder - Zfarming",
    page_icon="🪴",
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

def load_plant_data():
    try:
        df = pd.read_csv('data/plants.csv')
        return df
    except FileNotFoundError:
        st.error("Plant database not found. Please ensure the plants.csv file is in the data directory.")
        return pd.DataFrame()

def filter_plants(df, sunlight, space, care_level, plant_type):
    """Filter plants based on user preferences"""
    filtered = df.copy()
    
    # Filter by sunlight
    filtered = filtered[filtered['sunlight'] == sunlight]
    
    # Filter by space (handle different space options)
    space_mapping = {
        "Small Pot (Windowsill)": "Small Pot (Windowsill)",
        "Hanging Basket": "Hanging Basket", 
        "Medium Container": "Medium Container",
        "Large Container (Balcony)": "Large Container (Balcony)"
    }
    
    if space in space_mapping:
        filtered = filtered[filtered['space'] == space_mapping[space]]
    
    # Filter by care level
    filtered = filtered[filtered['care_level'] == care_level]
    
    # If no plants match exact criteria, show similar options
    if len(filtered) == 0:
        st.warning("No plants match your exact criteria. Here are some similar options:")
        # Show plants with same care level
        filtered = df[df['care_level'] == care_level].head(6)
    
    return filtered.head(6)  # Limit to 6 results

def display_results(plants):
    """Display filtered plant results as cards"""
    if plants.empty:
        st.warning("No plants found matching your criteria. Try adjusting your preferences!")
        return
    
    st.markdown("### 🌿 Your Perfect Plant Matches")
    st.markdown(f"Found **{len(plants)}** plants that match your preferences!")
    
    # Create plant cards in a grid
    cols = st.columns(2)
    
    for idx, (_, plant) in enumerate(plants.iterrows()):
        with cols[idx % 2]:
            with st.container():
                st.markdown(f'<div class="plant-card">', unsafe_allow_html=True)
                
                # Plant image
                try:
                    st.image(plant['image_url'], width=200, caption=plant['name'])
                except:
                    st.image("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=200&h=150&fit=crop", 
                            width=200, caption=plant['name'])
                
                # Plant name and tagline
                st.markdown(f"### {plant['name']}")
                st.markdown(f"*{plant['tagline']}*")
                
                # Quick stats
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("☀️ Sun", plant['sunlight'].split('(')[0].strip())
                with col2:
                    st.metric("💧 Water", plant['watering_frequency'])
                with col3:
                    st.metric("🏠 Space", plant['space'].split('(')[0].strip())
                
                # View guide button
                if st.button(f"📖 View {plant['name']} Guide", key=f"guide_{plant['plant_id']}", use_container_width=True):
                    st.session_state['selected_plant'] = plant['plant_id']
                    st.success(f"🎉 Great choice! {plant['name']} is perfect for your space!")
                    st.info("💡 Use the Plant Care Hub to find detailed care instructions.")
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")
    
    # Additional recommendations
    st.markdown("### 💡 Pro Tips for Your Plant Journey")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **🌱 Start Small**
        Begin with 1-2 plants to build confidence before expanding your collection.
        """)
    
    with col2:
        st.markdown("""
        **📅 Set Reminders**
        Use your phone to set watering reminders until caring becomes second nature.
        """)
    
    with col3:
        st.markdown("""
        **📚 Learn as You Grow**
        Each plant teaches you something new about gardening and plant care.
        """)

# Main content
st.markdown('<h1 class="main-header">🪴 Find My Perfect Plant</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover the ideal plants for your space and lifestyle! Answer a few questions and we\'ll recommend the perfect plants for you.</p>', unsafe_allow_html=True)

# Load plant data
plants_df = load_plant_data()

if plants_df.empty:
    st.stop()

# Create the form
st.markdown("### 🌟 Tell us about your space and lifestyle")

with st.form("plant_finder_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### ☀️ Sunlight")
        sunlight = st.select_slider(
            "How much sunlight does your space get?",
            options=["Low Light (No direct sun)", "Medium Light (A few hours)", "Bright Light (6+ hours)"],
            value="Medium Light (A few hours)"
        )
        
        st.markdown("#### 🏠 Space")
        space = st.radio(
            "What size container are you planning to use?",
            ["Small Pot (Windowsill)", "Hanging Basket", "Medium Container", "Large Container (Balcony)"]
        )
    
    with col2:
        st.markdown("#### 🌱 Care Level")
        care_level = st.selectbox(
            "How much time can you dedicate to plant care?",
            ["Beginner (I forget to water)", "Intermediate (I can follow a schedule)"]
        )
        
        st.markdown("#### 🎯 Plant Type")
        plant_type = st.multiselect(
            "What interests you most? (Select all that apply)",
            ["Herbs", "Flowers", "Vegetables", "Succulents", "Air Purifying", "Easy Care"]
        )
    
    # Submit button
    submitted = st.form_submit_button("🔍 Find My Perfect Plants!", type="primary", use_container_width=True)

if submitted:
    # Filter plants based on user preferences
    filtered_plants = filter_plants(plants_df, sunlight, space, care_level, plant_type)
    display_results(filtered_plants)
