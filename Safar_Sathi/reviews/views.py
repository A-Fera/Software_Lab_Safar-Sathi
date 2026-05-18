from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto
from .forms import DestinationReviewForm, AccommodationReviewForm, GuideReviewForm
from destinations.models import Destination
from bookings.models import Accommodation
from accounts.models import LocalGuide


def _save_review_photos(request, review):
    """Save uploaded photos to a review."""
    for f in request.FILES.getlist('photos'):
        photo = ReviewPhoto.objects.create(image=f)
        review.photos.add(photo)


@login_required
def destination_review_view(request, destination_id):
    if request.user.is_staff:
        messages.error(request, 'Admins cannot write reviews.')
        return redirect('destinations:destination_detail', pk=destination_id)
    destination = get_object_or_404(Destination, pk=destination_id)
    existing = DestinationReview.objects.filter(destination=destination, user=request.user).first()
    if request.method == 'POST':
        form = DestinationReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.destination = destination
            review.save()
            _save_review_photos(request, review)
            messages.success(request, 'Review submitted!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationReviewForm(instance=existing)
    return render(request, 'reviews/destination_review_form.html', {
        'form': form, 'destination': destination, 'existing': existing
    })


def destination_review_list_view(request, destination_id):
    destination = get_object_or_404(Destination, pk=destination_id)
    reviews = DestinationReview.objects.filter(
        destination=destination).select_related('user').prefetch_related('photos').order_by('-created_at')
    return render(request, 'reviews/destination_review_list.html', {
        'destination': destination, 'reviews': reviews
    })


@login_required
def accommodation_review_view(request, accommodation_id):
    if request.user.is_staff:
        messages.error(request, 'Admins cannot write reviews.')
        return redirect('bookings:accommodation_detail', accommodation_id)
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    existing = AccommodationReview.objects.filter(accommodation=accommodation, user=request.user).first()
    if request.method == 'POST':
        form = AccommodationReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.accommodation = accommodation
            review.save()
            _save_review_photos(request, review)
            accommodation.update_rating()
            messages.success(request, 'Review submitted!')
            return redirect('bookings:accommodation_detail', accommodation.pk)
    else:
        form = AccommodationReviewForm(instance=existing)
    return render(request, 'reviews/accommodation_review_form.html', {
        'form': form, 'accommodation': accommodation, 'existing': existing
    })


def accommodation_review_list_view(request, accommodation_id):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_id)
    reviews = AccommodationReview.objects.filter(
        accommodation=accommodation).select_related('user').prefetch_related('photos').order_by('-created_at')
    return render(request, 'reviews/accommodation_review_list.html', {
        'accommodation': accommodation, 'reviews': reviews
    })


@login_required
def guide_review_view(request, guide_id):
    if request.user.is_staff:
        messages.error(request, 'Admins cannot write reviews.')
        return redirect('accounts:guide_detail', pk=guide_id)
    guide = get_object_or_404(LocalGuide, pk=guide_id)
    existing = GuideReview.objects.filter(guide=guide, user=request.user).first()
    if request.method == 'POST':
        form = GuideReviewForm(request.POST, instance=existing)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.guide = guide
            review.save()
            _save_review_photos(request, review)
            guide.update_rating()
            messages.success(request, 'Review submitted!')
            return redirect('accounts:guide_detail', pk=guide.pk)
    else:
        form = GuideReviewForm(instance=existing)
    return render(request, 'reviews/guide_review_form.html', {
        'form': form, 'guide': guide, 'existing': existing
    })
