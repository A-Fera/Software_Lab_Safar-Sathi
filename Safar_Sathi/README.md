# Safar Sathi - Travel Companion Platform

A Django-based travel platform for exploring Bangladesh destinations.

## Quick Setup

### 1. Install Python 3.10+
Download from https://python.org

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Migrations
```bash
python manage.py migrate
```

### 5. Load Sample Data
```bash
python manage.py create_sample_data
```

### 6. Run Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Login Credentials
- **Admin**: username=`admin`, password=`admin123`
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Guide accounts**: password=`guide@2025`

## Features
- Destinations with photos and reviews
- Accommodations with ratings
- Local guides with profiles
- Itinerary planning
- User authentication
