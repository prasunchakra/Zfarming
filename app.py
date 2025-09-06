import streamlit as st

# Configure the page
st.set_page_config(
    page_title="Zfarming - Urban Garden Helper",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
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
    
    .feature-card {
        border: 2px solid #e0e0e0;
        border-radius: 15px;
        padding: 2rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.2s;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .cta-button {
        background: linear-gradient(45deg, #2E8B57, #32CD32);
        color: white;
        padding: 1rem 2rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .cta-button:hover {
        transform: scale(1.05);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">🌱 Zfarming</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Personal Urban Garden Assistant</p>', unsafe_allow_html=True)

# Hero section
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=800&h=400&fit=crop", 
            caption="Start your urban gardening journey today!")

st.markdown("---")

# Features overview
st.markdown("## 🌟 What Zfarming Can Do For You")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📸 Plant Scanner</h3>
        <p><strong>Identify any plant instantly!</strong></p>
        <p>Take a photo or upload an image of any plant leaf, and we'll tell you what it is with confidence scores.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🪴 Perfect Plant Finder</h3>
        <p><strong>Find your ideal plant match!</strong></p>
        <p>Answer a few questions about your space and lifestyle, and we'll recommend the perfect plants for you.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>📖 Plant Care Hub</h3>
        <p><strong>Expert care guides!</strong></p>
        <p>Get detailed, easy-to-follow care instructions for all your plants, from watering to troubleshooting.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Call to action
st.markdown("## 🚀 Ready to Start Your Garden?")

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <p style="font-size: 1.2rem; margin-bottom: 2rem;">Choose your adventure and begin your urban gardening journey!</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    if st.button("🔍 Identify a Plant", use_container_width=True, type="primary"):
        st.switch_page("pages/1_📸_Plant_Scanner.py")

with col2:
    if st.button("🪴 Find My Plant", use_container_width=True, type="primary"):
        st.switch_page("pages/2_🪴_Perfect_Plant_Finder.py")

with col3:
    if st.button("📚 Browse Guides", use_container_width=True, type="primary"):
        st.switch_page("pages/3_📖_Plant_Care_Hub.py")

st.markdown("---")

# Additional information
st.markdown("## 🌱 About Zfarming")

st.markdown("""
Zfarming is designed to make urban gardening accessible and enjoyable for everyone. Whether you're a complete beginner or have some gardening experience, our tools will help you:

- **Identify plants** you find in your neighborhood or garden
- **Discover the perfect plants** for your specific living space
- **Learn proper care techniques** with detailed, easy-to-follow guides
- **Build confidence** in your gardening abilities

Our database includes 15+ urban-friendly plants, from easy-care succulents to fresh herbs and vegetables you can grow right in your home.
""")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; margin-top: 2rem;">
    <p>🌱 <strong>Zfarming</strong> - Making urban gardening simple and fun!</p>
    <p>Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
