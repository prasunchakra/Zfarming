import streamlit as st
import pandas as pd

# Configure the page
st.set_page_config(
    page_title="Plant Care Hub - Zfarming",
    page_icon="📖",
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
    
    .stats-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .guide-section {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
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

def show_plant_selection(plants_df):
    """Show plant selection interface"""
    st.markdown("### 🌱 Choose a Plant to Learn About")
    
    # Search and filter options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search for a plant:", placeholder="Type plant name...")
    
    with col2:
        care_level_filter = st.selectbox("Filter by care level:", ["All", "Beginner", "Intermediate"])
    
    # Filter plants
    filtered_plants = plants_df.copy()
    
    if search_term:
        filtered_plants = filtered_plants[
            filtered_plants['name'].str.contains(search_term, case=False, na=False) |
            filtered_plants['scientific_name'].str.contains(search_term, case=False, na=False)
        ]
    
    if care_level_filter != "All":
        filtered_plants = filtered_plants[filtered_plants['care_level'].str.contains(care_level_filter, na=False)]
    
    if filtered_plants.empty:
        st.warning("No plants found matching your search criteria.")
        return
    
    # Display plants in a grid
    st.markdown(f"**Found {len(filtered_plants)} plants:**")
    
    cols = st.columns(3)
    
    for idx, (_, plant) in enumerate(filtered_plants.iterrows()):
        with cols[idx % 3]:
            with st.container():
                st.markdown(f'<div class="plant-card">', unsafe_allow_html=True)
                
                # Plant image
                try:
                    st.image(plant['image_url'], width=150, caption=plant['name'])
                except:
                    st.image("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=150&h=100&fit=crop", 
                            width=150, caption=plant['name'])
                
                # Plant name and basic info
                st.markdown(f"**{plant['name']}**")
                st.markdown(f"*{plant['scientific_name']}*")
                
                # Quick stats
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("☀️", plant['sunlight'].split('(')[0].strip())
                with col2:
                    st.metric("💧", plant['watering_frequency'])
                
                # View guide button
                if st.button(f"📖 View Guide", key=f"guide_{plant['plant_id']}", use_container_width=True):
                    st.session_state['selected_plant'] = plant['plant_id']
                    st.rerun()
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown("---")

def show_plant_guide(plant):
    """Show detailed plant care guide"""
    # Header with plant image and basic info
    col1, col2 = st.columns([1, 2])
    
    with col1:
        try:
            st.image(plant['image_url'], width=300)
        except:
            st.image("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=200&fit=crop")
    
    with col2:
        st.markdown(f"# {plant['name']}")
        st.markdown(f"### *{plant['scientific_name']}*")
        st.markdown(f"**{plant['tagline']}**")
        st.markdown(plant['description'])
    
    # Back button
    if st.button("← Back to Plant Selection"):
        if 'selected_plant' in st.session_state:
            del st.session_state['selected_plant']
        st.rerun()
    
    st.markdown("---")
    
    # Quick Stats section
    st.markdown("### 📊 Quick Stats")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="stats-container">
            <h4>☀️ Sunlight Needs</h4>
            <p><strong>{plant['sunlight']}</strong></p>
            <p>{plant['sunlight_needs']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stats-container">
            <h4>💧 Watering</h4>
            <p><strong>{plant['watering_frequency']}</strong></p>
            <p>Keep soil {plant['watering_guide'].lower()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stats-container">
            <h4>🏠 Pot Size</h4>
            <p><strong>{plant['pot_size']}</strong></p>
            <p>Perfect for {plant['space'].lower()}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed care sections
    st.markdown("### 📚 Detailed Care Guide")
    
    # Watering Guide
    with st.expander("💧 Watering Guide", expanded=True):
        st.markdown(f"""
        <div class="guide-section">
            <h4>How Often to Water</h4>
            <p><strong>Frequency:</strong> {plant['watering_frequency']}</p>
            <p><strong>Method:</strong> {plant['watering_guide']}</p>
            
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>Check soil moisture by sticking your finger 1 inch into the soil</li>
                <li>Water until you see water coming out of the drainage holes</li>
                <li>Empty the saucer after watering to prevent root rot</li>
                <li>Use room temperature water for best results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Sunlight Needs
    with st.expander("☀️ Sunlight Needs"):
        st.markdown(f"""
        <div class="guide-section">
            <h4>Light Requirements</h4>
            <p><strong>Ideal Light:</strong> {plant['sunlight']}</p>
            <p><strong>Details:</strong> {plant['sunlight_guide']}</p>
            
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>Rotate your plant weekly to ensure even growth</li>
                <li>Watch for signs of too much light (brown, crispy leaves)</li>
                <li>Watch for signs of too little light (stretching, pale leaves)</li>
                <li>Consider using a grow light if natural light is insufficient</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Potting Tips
    with st.expander("🏺 Potting Tips"):
        st.markdown(f"""
        <div class="guide-section">
            <h4>Container & Soil</h4>
            <p><strong>Recommended Pot Size:</strong> {plant['pot_size']}</p>
            <p><strong>Space Requirements:</strong> {plant['space']}</p>
            <p><strong>Soil Tips:</strong> {plant['potting_tips']}</p>
            
            <h4>💡 Pro Tips</h4>
            <ul>
                <li>Choose pots with drainage holes to prevent waterlogging</li>
                <li>Use well-draining potting mix appropriate for your plant type</li>
                <li>Repot when roots start growing out of drainage holes</li>
                <li>Clean pots between uses to prevent disease spread</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Common Issues
    with st.expander("⚠️ Common Issues & Solutions"):
        st.markdown(f"""
        <div class="guide-section">
            <h4>Watch Out For</h4>
            <p><strong>Common Problems:</strong> {plant['common_issues']}</p>
            
            <h4>🔧 Troubleshooting Guide</h4>
            <ul>
                <li><strong>Yellow leaves:</strong> Usually overwatering or poor drainage</li>
                <li><strong>Brown leaf tips:</strong> Often low humidity or over-fertilization</li>
                <li><strong>Drooping leaves:</strong> Check soil moisture and light levels</li>
                <li><strong>No new growth:</strong> May need more light or fertilizer</li>
                <li><strong>Pests:</strong> Check undersides of leaves regularly</li>
            </ul>
            
            <h4>🚨 When to Seek Help</h4>
            <p>If your plant shows severe symptoms or doesn't improve after adjusting care, 
            consider consulting a local nursery or plant expert.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Additional Resources
    st.markdown("### 🌟 Additional Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **📱 Plant Care Apps**
        - PlantNet (plant identification)
        - Planta (care reminders)
        - Garden Answers (plant Q&A)
        """)
    
    with col2:
        st.markdown("""
        **🌐 Online Communities**
        - r/houseplants (Reddit)
        - Plant Care Facebook groups
        - Local gardening clubs
        """)
    
    # Plant care calendar (simplified)
    st.markdown("### 📅 Monthly Care Calendar")
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # Create a simple calendar view
    calendar_cols = st.columns(4)
    
    for i, month in enumerate(months):
        with calendar_cols[i % 4]:
            st.markdown(f"**{month}**")
            if plant['care_level'] == "Beginner (I forget to water)":
                st.markdown("🌱 Water less in winter")
            else:
                st.markdown("🌱 Regular care schedule")
    
    # Action buttons
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🔄 Refresh Guide", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📋 Print Guide", use_container_width=True):
            st.info("💡 Use your browser's print function to save this guide!")
    
    with col3:
        if st.button("🏠 Back to Home", use_container_width=True):
            if 'selected_plant' in st.session_state:
                del st.session_state['selected_plant']
            st.switch_page("app.py")

# Main content
st.markdown('<h1 class="main-header">📖 Plant Care Hub</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your comprehensive guide to plant care! Find detailed instructions for all your plants.</p>', unsafe_allow_html=True)

# Load plant data
plants_df = load_plant_data()

if plants_df.empty:
    st.stop()

# Check if a specific plant was selected
if 'selected_plant' in st.session_state:
    plant_id = st.session_state['selected_plant']
    plant = plants_df[plants_df['plant_id'] == plant_id]
    if not plant.empty:
        show_plant_guide(plant.iloc[0])
    else:
        show_plant_selection(plants_df)
else:
    # Show plant selection interface
    show_plant_selection(plants_df)
