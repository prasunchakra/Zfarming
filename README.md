# 🌱 Zfarming - Urban Garden Helper

A proof-of-concept (POC) web application built with Streamlit to help urban residents start their own small-scale gardens. This interactive tool provides plant identification, personalized plant recommendations, and comprehensive care guides.

## ✨ Features

### 📸 Plant Scanner
- **Camera Integration**: Take photos or upload images of plant leaves
- **AI-Powered Identification**: Identify plants using advanced plant recognition
- **Confidence Scores**: Get detailed results with confidence ratings
- **Quick Access**: Direct links to care guides for identified plants

### 🪴 Perfect Plant Finder
- **Personalized Recommendations**: Find plants based on your space and lifestyle
- **Interactive Form**: Answer questions about sunlight, space, and care level
- **Visual Results**: Browse recommended plants in an attractive card layout
- **Smart Filtering**: Get plants that match your exact preferences

### 📖 Plant Care Hub
- **Comprehensive Guides**: Detailed care instructions for 15+ starter plants
- **Quick Stats**: At-a-glance information about sunlight, watering, and pot size
- **Expandable Sections**: Organized information in collapsible sections
- **Troubleshooting**: Common issues and solutions for each plant

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Zfarming
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` to view the application.

## 📁 Project Structure

```
Zfarming/
├── app.py                          # Main application entry point
├── requirements.txt                # Python dependencies
├── README.md                      # Project documentation
├── .streamlit/
│   └── config.toml                # Streamlit configuration
├── pages/                         # Multi-page application modules
│   ├── __init__.py
│   ├── plant_scanner.py          # Plant identification module
│   ├── plant_finder.py           # Plant recommendation module
│   └── plant_care_hub.py         # Plant care guides module
└── data/
    └── plants.csv                 # Plant database with care information
```

## 🌿 Plant Database

The application includes a comprehensive database of 15+ urban-friendly plants:

- **Herbs**: Mint, Basil, Parsley, Cilantro, Rosemary, Lavender
- **Flowers**: Marigold, Peace Lily
- **Vegetables**: Cherry Tomatoes, Chilli, Lettuce
- **Succulents**: Snake Plant, Aloe Vera
- **Air Purifying**: Snake Plant, Spider Plant, Peace Lily

Each plant entry includes:
- Scientific and common names
- Sunlight requirements
- Space needs
- Care difficulty level
- Watering frequency
- Detailed care instructions
- Common issues and solutions

## 🔧 API Integration

### Plant Identification
The app is designed to integrate with plant identification APIs:

- **Plant.id**: Primary recommendation (free tier available)
- **Pl@ntNet**: Alternative option
- **Custom API**: Easy to integrate with other services

**Note**: For the POC, the app uses simulated results. To enable real plant identification:

1. Sign up for a Plant.id API key
2. Update the `call_plant_id_api()` function in `plant_scanner.py`
3. Add your API key to environment variables

## 🎨 Design Features

- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, intuitive interface with plant-themed colors
- **Interactive Elements**: Engaging forms, buttons, and navigation
- **Visual Feedback**: Progress bars, success messages, and helpful tips
- **Accessibility**: Clear typography and color contrast

## 🛠️ Customization

### Adding New Plants
1. Edit `data/plants.csv` to add new plant entries
2. Include all required columns: name, scientific_name, sunlight, space, care_level, etc.
3. Add high-quality images (URLs) for best visual appeal

### Modifying Plant Care Information
- Update the CSV file with new care instructions
- Modify the display logic in `plant_care_hub.py` if needed
- Add new care categories by updating the expandable sections

### Styling Changes
- Modify CSS in `app.py` for global styling
- Update `.streamlit/config.toml` for theme customization
- Customize individual page layouts in respective module files

## 📱 Mobile Optimization

The application is fully responsive and optimized for mobile devices:
- Touch-friendly interface elements
- Optimized image sizes for mobile viewing
- Responsive grid layouts
- Mobile-friendly navigation

## 🔮 Future Enhancements

- **Real API Integration**: Connect to actual plant identification services
- **User Accounts**: Save favorite plants and care schedules
- **Plant Care Reminders**: Push notifications for watering schedules
- **Community Features**: Share plant photos and tips
- **Advanced Filtering**: More sophisticated plant recommendation algorithms
- **Plant Health Monitoring**: Track plant growth and health over time

## 🤝 Contributing

This is a POC project, but contributions are welcome! Areas for improvement:
- Additional plant species
- Enhanced plant identification accuracy
- Improved mobile experience
- Additional care guide content
- Performance optimizations

## 📄 License

This project is created for educational and demonstration purposes.

## 🙏 Acknowledgments

- **Plant Images**: Unsplash for high-quality plant photography
- **Plant Data**: Compiled from various gardening resources
- **Streamlit**: For the excellent web app framework
- **Plant Identification APIs**: Plant.id and Pl@ntNet for inspiration

---

**Happy Gardening! 🌱**
