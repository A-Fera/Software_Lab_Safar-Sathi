from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.home, name='home'),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('destinations/', include('destinations.urls', namespace='destinations')),
    path('bookings/', include('bookings.urls', namespace='bookings')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('itinerary/', include('itinerary.urls', namespace='itinerary')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
