from django.db import models
from accounts.models import CustomUser, LocalGuide
from destinations.models import Destination

class AccommodationPhoto(models.Model):
    image = models.ImageField(upload_to='accommodations/photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo {self.pk}"

class Accommodation(models.Model):
    ACCOMMODATION_TYPES = [
        ('hotel', 'Hotel'),
        ('resort', 'Resort'),
        ('guesthouse', 'Guest House'),
        ('hostel', 'Hostel'),
        ('cottage', 'Cottage'),
        ('apartment', 'Apartment'),
        ('other', 'Other'),
    ]

    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='accommodations')
    name = models.CharField(max_length=200)
    accommodation_type = models.CharField(max_length=50, choices=ACCOMMODATION_TYPES, default='hotel')
    location = models.CharField(max_length=300, blank=True)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    max_guests = models.IntegerField(default=2)
    check_in_time = models.TimeField(default='14:00')
    check_out_time = models.TimeField(default='11:00')
    photos = models.ManyToManyField(AccommodationPhoto, blank=True, related_name='accommodations')
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_accommodation_type_display(self):
        return dict(self.ACCOMMODATION_TYPES).get(self.accommodation_type, self.accommodation_type)

    def update_rating(self):
        from reviews.models import AccommodationReview
        reviews = AccommodationReview.objects.filter(accommodation=self)
        if reviews.exists():
            from django.db.models import Avg
            avg = reviews.aggregate(Avg('rating'))['rating__avg']
            self.rating = round(avg, 1)
            self.save()

    def first_photo(self):
        return self.photos.first()

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='bookings')
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    guide = models.ForeignKey(LocalGuide, on_delete=models.SET_NULL, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking #{self.pk} by {self.user.username}"

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('bkash', 'bKash'),
        ('nagad', 'Nagad'),
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    transaction_id = models.CharField(max_length=200, blank=True)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='cash')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Booking #{self.booking.pk}"

    def get_payment_method_display(self):
        return dict(self.PAYMENT_METHODS).get(self.payment_method, self.payment_method)

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)
