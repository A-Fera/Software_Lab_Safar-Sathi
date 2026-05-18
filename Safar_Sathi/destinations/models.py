from django.db import models
from accounts.models import CustomUser

DIVISION_CHOICES = [
    ('dhaka', 'Dhaka'),
    ('chittagong', 'Chittagong'),
    ('rajshahi', 'Rajshahi'),
    ('khulna', 'Khulna'),
    ('barisal', 'Barisal'),
    ('sylhet', 'Sylhet'),
    ('rangpur', 'Rangpur'),
    ('mymensingh', 'Mymensingh'),
]

class Destination(models.Model):
    CATEGORY_CHOICES = [
        ('beach', 'Beach'),
        ('mountain', 'Mountain'),
        ('forest', 'Forest'),
        ('historical', 'Historical'),
        ('urban', 'Urban'),
        ('rural', 'Rural'),
        ('river', 'River'),
        ('wildlife', 'Wildlife'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    division = models.CharField(max_length=100, choices=DIVISION_CHOICES, blank=True)
    country = models.CharField(max_length=100, default='Bangladesh')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    best_time_to_visit = models.CharField(max_length=200, blank=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='destinations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_category_display(self):
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)

    def get_division_display(self):
        return dict(DIVISION_CHOICES).get(self.division, self.division)

class DestinationFeature(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='features')
    feature_name = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.destination.name} - {self.feature_name}"

class Photo(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='photos')
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='destinations/photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.destination.name}"
