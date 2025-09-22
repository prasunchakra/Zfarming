# 🌱 ZFarming - Production Django Application

A production-grade Django web application converted from the original Streamlit POC. ZFarming helps urban residents start their own small-scale gardens with plant identification, personalized recommendations, and comprehensive care guides.

## ✨ Features

### 🎯 Core Functionality
- **Plant Scanner**: AI-powered plant identification using camera or image upload
- **Perfect Plant Finder**: Personalized plant recommendations based on user preferences
- **Plant Care Hub**: Comprehensive care guides with detailed instructions
- **User Accounts**: Profile management, plant collections, and history tracking
- **Admin Interface**: Complete plant database management

### 🚀 Production Features
- **Security**: HTTPS, CSRF protection, secure headers, and input validation
- **Performance**: Database optimization, caching, static file compression
- **Scalability**: Docker containerization, database migrations, CI/CD ready
- **Monitoring**: Comprehensive logging and error tracking
- **Mobile-First**: Responsive design optimized for all devices

## 🛠️ Technology Stack

- **Backend**: Django 4.2, Python 3.11
- **Database**: PostgreSQL (production), SQLite (development)
- **Frontend**: Bootstrap 5, vanilla JavaScript, responsive design
- **APIs**: Plant.id integration for plant identification
- **Deployment**: Docker, Gunicorn, Nginx
- **Storage**: Local files (development), AWS S3 (production)
- **Caching**: Redis for session storage and caching

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL (for production)
- Redis (for production caching)
- Docker & Docker Compose (optional)

## 🚀 Quick Start

### Development Setup

1. **Clone and Setup**
   ```bash
   cd zfarming_django
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cp env_example.txt .env
   # Edit .env with your configuration
   ```

3. **Database Setup**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

4. **Load Initial Data**
   ```bash
   python data_migration.py
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

Visit `http://localhost:8000` to access the application.

### Docker Setup

1. **Using Docker Compose**
   ```bash
   docker-compose up -d
   ```

2. **Initialize Database**
   ```bash
   docker-compose exec web python manage.py migrate
   docker-compose exec web python manage.py createsuperuser
   docker-compose exec web python data_migration.py
   ```

## 📊 Database Schema

### Core Models
- **Plant**: Complete plant information and care details
- **PlantCategory**: Categorization (Herbs, Flowers, Vegetables, etc.)
- **PlantCareGuide**: Extended care instructions and calendars
- **User**: Custom user model with gardening preferences
- **UserPlantCollection**: Track user's plants and their status
- **PlantIdentificationHistory**: Store identification attempts and results

### Key Features
- **Optimized Queries**: Database indexes on frequently searched fields
- **Data Integrity**: Foreign key constraints and validation
- **Audit Trail**: Created/updated timestamps on all models
- **Flexible Storage**: Support for both local and cloud image storage

## 🔧 Configuration

### Environment Variables

```bash
# Core Django Settings
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgres://user:password@localhost:5432/zfarming

# External APIs
PLANT_ID_API_KEY=your-plant-id-api-key

# Email (Production)
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-password

# Redis Caching
REDIS_URL=redis://localhost:6379/0

# AWS S3 (Production)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### Plant.id API Setup

1. Sign up at [Plant.id](https://web.plant.id/)
2. Get your API key
3. Add to environment variables: `PLANT_ID_API_KEY=your-key`

## 📱 Key Features

### 🔍 Plant Scanner
- Real-time plant identification using Plant.id API
- Confidence scoring and multiple suggestions
- Integration with plant database for care information
- Image upload with preview and validation
- History tracking for authenticated users

### 🎯 Plant Finder
- Interactive questionnaire for preferences
- Smart filtering based on sunlight, space, and care level
- Personalized recommendations with visual cards
- Integration with user profiles and collections

### 📚 Care Hub
- Comprehensive plant care guides
- Monthly care calendars
- Troubleshooting guides
- Expert tips and common mistakes
- Printable care instructions

### 👤 User Management
- Custom user model with gardening preferences
- Plant collection tracking (want to grow, currently growing, etc.)
- Identification history with user feedback
- Profile management and preferences

## 🔒 Security Features

- **HTTPS Enforcement**: Secure communication in production
- **CSRF Protection**: All forms protected against CSRF attacks
- **Input Validation**: Server-side validation for all user inputs
- **SQL Injection Prevention**: Django ORM prevents SQL injection
- **XSS Protection**: Template auto-escaping and secure headers
- **File Upload Security**: Image validation and secure storage
- **Rate Limiting**: API rate limiting for external requests

## 🎨 Design System

### Responsive Design
- Mobile-first approach with Bootstrap 5
- Touch-friendly interface elements
- Optimized images and fast loading
- Accessible color contrast and typography

### User Experience
- Intuitive navigation with clear visual hierarchy
- Progressive enhancement with JavaScript
- Loading states and user feedback
- Error handling with helpful messages

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure secure database (PostgreSQL)
- [ ] Set up Redis for caching
- [ ] Configure email backend
- [ ] Set up static file serving (S3 or CDN)
- [ ] Configure logging and monitoring
- [ ] Set up SSL certificates
- [ ] Configure backup strategy

### Docker Deployment
```bash
# Build and deploy
docker-compose -f docker-compose.prod.yml up -d

# Database migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput
```

## 📈 Performance Optimization

### Database
- Optimized queries with select_related and prefetch_related
- Database indexes on frequently searched fields
- Connection pooling and query optimization

### Caching
- Redis for session storage and view caching
- Template fragment caching for expensive operations
- Static file compression and CDN integration

### Frontend
- Minified CSS and JavaScript
- Image optimization and lazy loading
- Progressive Web App features

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.plants

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 📝 API Documentation

### Plant Identification API
```python
POST /api/scanner/identify/
Content-Type: multipart/form-data

{
    "image": <image_file>,
    "confidence_threshold": 0.5
}
```

### Plant Search API
```python
GET /api/plants/?search=basil&care_level=beginner&sunlight=medium
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

### Code Style
- Follow PEP 8 for Python code
- Use Black for code formatting
- Add docstrings for all functions and classes
- Write comprehensive tests

## 📄 License

This project is created for educational and demonstration purposes. See the original Streamlit POC for licensing information.

## 🙏 Acknowledgments

- **Original Streamlit POC**: Foundation for this Django conversion
- **Plant.id API**: Plant identification service
- **Unsplash**: High-quality plant photography
- **Django Community**: Excellent framework and documentation
- **Bootstrap**: Responsive UI framework

## 📞 Support

For support and questions:
- Check the documentation
- Review existing issues
- Create a new issue with detailed information

---

**Happy Gardening with ZFarming! 🌱**
