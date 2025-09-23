#!/bin/bash

# ZFarming Django Setup Script
# This script sets up the Django application for development

set -e

echo "🌱 Setting up ZFarming Django Application..."

# Check if Python 3.11+ is available
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $python_version"

if ! python3 -c 'import sys; exit(not (sys.version_info[0] == 3 and sys.version_info[1] >= 11))'; then
    echo "❌ Python 3.11+ is required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs media staticfiles

# Environment setup
if [ ! -f ".env" ]; then
    echo "⚙️ Creating environment file..."
    cp env_example.txt .env
    echo "✏️ Please edit .env file with your configuration"
fi

# Database migrations
echo "🗃️ Running database migrations..."
python manage.py migrate

# Create logs directory and set permissions
mkdir -p logs
touch logs/django.log

# Collect static files
echo "🎨 Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser (optional)
echo "👤 Do you want to create a superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ] || [ "$create_superuser" = "Y" ]; then
    python manage.py createsuperuser
fi

# Load initial data
echo "📊 Do you want to load initial plant data? (y/n)"
read -r load_data
if [ "$load_data" = "y" ] || [ "$load_data" = "Y" ]; then
    if [ -f "data/plants.csv" ]; then
        python data_migration.py
        echo "✅ Initial plant data loaded successfully!"
    else
        echo "⚠️ Plant data CSV not found at data/plants.csv"
        echo "   Please ensure the data file is available"
    fi
fi

echo ""
echo "🎉 Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Edit .env file with your configuration"
echo "2. Get Plant.id API key and add to .env"
echo "3. Run: python manage.py runserver"
echo "4. Visit: http://localhost:8000"
echo ""
echo "📚 Documentation:"
echo "- Admin panel: http://localhost:8000/admin/"
echo "- API docs: http://localhost:8000/api/"
echo "- Plant scanner: http://localhost:8000/scanner/"
echo "- Plant finder: http://localhost:8000/finder/"
echo "- Care hub: http://localhost:8000/care/"
echo ""
echo "🌱 Happy gardening with ZFarming!"
