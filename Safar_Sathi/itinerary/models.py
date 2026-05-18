from django.db import models
from accounts.models import CustomUser
from destinations.models import Destination
from bookings.models import Accommodation

class Itinerary(models.Model):
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('confirmed', 'Confirmed'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='itineraries')
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or self.name

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = self.name
        super().save(*args, **kwargs)

    @property
    def total_days(self):
        return (self.end_date - self.start_date).days + 1

    @property
    def total_destinations(self):
        return self.items.filter(destination__isnull=False).values('destination').distinct().count()

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_cost(self):
        total = self.items.aggregate(models.Sum('estimated_cost'))['estimated_cost__sum']
        return total or 0

    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, self.status)


class ItineraryItem(models.Model):
    ITEM_TYPES = [
        ('destination', 'Destination Visit'),
        ('accommodation', 'Accommodation'),
        ('transport', 'Transport'),
        ('activity', 'Activity'),
        ('meal', 'Meal'),
        ('other', 'Other'),
    ]

    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='items')
    destination = models.ForeignKey(Destination, on_delete=models.SET_NULL, null=True, blank=True)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.SET_NULL, null=True, blank=True)
    item_type = models.CharField(max_length=50, choices=ITEM_TYPES, default='destination')
    title = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_date']

    def __str__(self):
        return self.title

    def get_item_type_display(self):
        return dict(self.ITEM_TYPES).get(self.item_type, self.item_type)
