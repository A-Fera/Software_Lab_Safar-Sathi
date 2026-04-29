from django.shortcuts import render
from destinations.models import Destination
from accounts.models import LocalGuide

def home(request):
    featured_destinations = Destination.objects.filter(is_featured=True)[:6]
    top_guides = LocalGuide.objects.all()[:4]
    context = {
        'featured_destinations': featured_destinations,
        'top_guides': top_guides,
    }
    return render(request, 'home.html', context)
