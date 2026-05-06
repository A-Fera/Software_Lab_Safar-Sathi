from django.contrib import admin
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto

admin.site.register(DestinationReview)
admin.site.register(AccommodationReview)
admin.site.register(GuideReview)
admin.site.register(ReviewPhoto)
