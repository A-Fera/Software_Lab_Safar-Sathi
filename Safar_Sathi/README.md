# Safar Sathi — Your Travel Companion 🧭

A full-featured Django travel platform for exploring Bangladesh destinations, booking accommodations, hiring local guides, writing reviews, and planning itineraries.

---

## Features

- 🗺️ Destination discovery with photos, categories, and reviews
- 🏨 Accommodation listings with booking and payment flow
- 👨‍🦯 Local guide profiles and ratings
- ⭐ Reviews for destinations, accommodations, and guides
- 📋 Trip itinerary planner
- 👤 User authentication and profile management
- 🔑 Admin panel for content management

---

## Quick Setup in PyCharm

### 1. Open Project
Open the `safar_sathi/` folder in PyCharm.

### 2. Create Virtual Environment
In PyCharm terminal:
```bash
python -m venv venv
```
Activate it:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply Migrations
```bash
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```
Enter a username, email, and password when prompted.

### 6. (Optional) Load Sample Data
```bash
python manage.py create_sample_data
```

### 7. Run the Server
```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000/**

Admin panel: **http://127.0.0.1:8000/admin/**

---

## Project Structure

```
safar_sathi/
├── accounts/          # User auth, profiles, local guides
├── bookings/          # Accommodations, bookings, payments
├── destinations/      # Destinations and photos
├── itinerary/         # Trip planning
├── reviews/           # Reviews for all entities
├── safar_sathi/       # Main settings and URLs
├── templates/         # All HTML templates
├── static/            # Static files
├── media/             # Uploaded images
├── manage.py
└── requirements.txt
```

---

## Default Admin Credentials (after createsuperuser)
Use the credentials you set during `createsuperuser`.

## Tech Stack
- **Backend:** Django 4.2
- **Frontend:** Bootstrap 5.3 + Bootstrap Icons
- **Database:** SQLite (development)
- **Font:** Inter + Playfair Display (Google Fonts)

