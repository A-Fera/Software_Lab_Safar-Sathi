from django.db import models
from accounts.models import CustomUser, LocalGuide
from destinations.models import Destination

class ReviewPhoto(models.Model):
    image = models.ImageField(upload_to='reviews/photos/')
    caption = models.CharField(max_length=300, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review Photo {self.pk}"

class DestinationReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200, default='My Review')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    photos = models.ManyToManyField(ReviewPhoto, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'destination']

    def __str__(self):
        return f"Review of {self.destination.name} by {self.user.username}"

class AccommodationReview(models.Model):
    from bookings.models import Accommodation
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    accommodation = models.ForeignKey('bookings.Accommodation', on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200, default='My Review')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    photos = models.ManyToManyField(ReviewPhoto, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'accommodation']

    def __str__(self):
        return f"Review of {self.accommodation.name} by {self.user.username}"

class GuideReview(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    guide = models.ForeignKey(LocalGuide, on_delete=models.CASCADE, related_name='reviews')
    title = models.CharField(max_length=200, default='My Review')
    content = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    photos = models.ManyToManyField(ReviewPhoto, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'guide']

    def __str__(self):
        return f"Review of guide {self.guide} by {self.user.username}"
