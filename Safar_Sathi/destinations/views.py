from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView
from .models import Destination, Photo, DIVISION_CHOICES
from .forms import DestinationForm, PhotoUploadForm


def staff_required(user):
    return user.is_staff


class DestinationListView(ListView):
    model = Destination
    template_name = 'destinations/destination_list.html'
    context_object_name = 'destinations'
    paginate_by = 9

    def get_queryset(self):
        qs = Destination.objects.all()
        search = self.request.GET.get('search', '').strip()
        category = self.request.GET.get('category', '')
        division = self.request.GET.get('division', '')
        if search:
            qs = qs.filter(name__icontains=search) | qs.filter(location__icontains=search)
        if category:
            qs = qs.filter(category=category)
        if division:
            qs = qs.filter(division=division)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['categories'] = Destination.CATEGORY_CHOICES
        ctx['divisions'] = DIVISION_CHOICES
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_category'] = self.request.GET.get('category', '')
        ctx['selected_division'] = self.request.GET.get('division', '')
        return ctx


def destination_detail_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    photos = destination.photos.all()
    accommodations = destination.accommodations.all()
    reviews = destination.reviews.select_related('user').order_by('-created_at')[:5]
    user_has_reviewed = False
    if request.user.is_authenticated and not request.user.is_staff:
        from reviews.models import DestinationReview
        user_has_reviewed = DestinationReview.objects.filter(
            destination=destination, user=request.user).exists()
    return render(request, 'destinations/destination_detail.html', {
        'destination': destination,
        'photos': photos,
        'accommodations': accommodations,
        'reviews': reviews,
        'user_has_reviewed': user_has_reviewed,
    })


@user_passes_test(staff_required)
def destination_create_view(request):
    if request.method == 'POST':
        form = DestinationForm(request.POST)
        if form.is_valid():
            dest = form.save(commit=False)
            dest.created_by = request.user
            dest.save()
            # Handle multiple photos from raw HTML file input
            for f in request.FILES.getlist('images'):
                Photo.objects.create(destination=dest, user=request.user, image=f)
            messages.success(request, 'Destination created!')
            return redirect('destinations:destination_detail', pk=dest.pk)
    else:
        form = DestinationForm()
    return render(request, 'destinations/destination_form.html',
                  {'form': form, 'title': 'Add Destination'})


@user_passes_test(staff_required)
def destination_update_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        form = DestinationForm(request.POST, instance=destination)
        if form.is_valid():
            form.save()
            for f in request.FILES.getlist('images'):
                Photo.objects.create(destination=destination, user=request.user, image=f)
            messages.success(request, 'Destination updated!')
            return redirect('destinations:destination_detail', pk=destination.pk)
    else:
        form = DestinationForm(instance=destination)
    return render(request, 'destinations/destination_form.html',
                  {'form': form, 'title': 'Edit Destination', 'destination': destination})


@user_passes_test(staff_required)
def destination_delete_view(request, pk):
    destination = get_object_or_404(Destination, pk=pk)
    if request.method == 'POST':
        destination.delete()
        messages.success(request, 'Destination deleted.')
        return redirect('destinations:destination_list')
    return render(request, 'destinations/destination_confirm_delete.html',
                  {'destination': destination})


@login_required
def photo_upload_view(request, destination_pk):
    """Upload multiple photos from inside the destination detail page (admin only)."""
    destination = get_object_or_404(Destination, pk=destination_pk)
    if not request.user.is_staff:
        messages.error(request, 'Only admins can upload destination photos.')
        return redirect('destinations:destination_detail', pk=destination_pk)
    if request.method == 'POST':
        files = request.FILES.getlist('images')
        if files:
            for f in files:
                Photo.objects.create(destination=destination, user=request.user, image=f)
            messages.success(request, f'{len(files)} photo(s) uploaded!')
        else:
            messages.warning(request, 'No photos selected.')
    return redirect('destinations:destination_detail', pk=destination_pk)
