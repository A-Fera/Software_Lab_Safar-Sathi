from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.generic import ListView
from django.db.models import Q
from .models import Accommodation, Booking, Payment
from .forms import AccommodationForm, BookingForm, PaymentForm
from reviews.models import AccommodationReview

def staff_required(user):
    return user.is_staff

class AccommodationListView(ListView):
    model = Accommodation
    template_name = 'bookings/accommodation_list.html'
    context_object_name = 'accommodations'
    paginate_by = 9

    def get_queryset(self):
        qs = Accommodation.objects.select_related('destination').all()
        search = self.request.GET.get('search')
        actype = self.request.GET.get('type')
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(destination__name__icontains=search))
        if actype:
            qs = qs.filter(accommodation_type=actype)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['accommodation_types'] = Accommodation.ACCOMMODATION_TYPES
        ctx['search'] = self.request.GET.get('search', '')
        ctx['selected_type'] = self.request.GET.get('type', '')
        return ctx

def accommodation_detail_view(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    reviews = AccommodationReview.objects.filter(accommodation=accommodation).select_related('user').prefetch_related('photos')[:10]
    user_can_review = False
    if request.user.is_authenticated:
        user_can_review = not AccommodationReview.objects.filter(accommodation=accommodation, user=request.user).exists()
    return render(request, 'bookings/accommodation_detail.html', {
        'accommodation': accommodation,
        'reviews': reviews,
        'user_can_review': user_can_review,
    })

@user_passes_test(staff_required)
def accommodation_create_view(request):
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES)
        if form.is_valid():
            acc = form.save(commit=False)
            acc.created_by = request.user
            acc.save()
            messages.success(request, 'Accommodation created!')
            return redirect('bookings:accommodation_detail', pk=acc.pk)
    else:
        form = AccommodationForm()
    return render(request, 'bookings/accommodation_form.html', {'form': form, 'title': 'Add Accommodation'})

@user_passes_test(staff_required)
def accommodation_update_view(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    if request.method == 'POST':
        form = AccommodationForm(request.POST, request.FILES, instance=accommodation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Accommodation updated!')
            return redirect('bookings:accommodation_detail', pk=accommodation.pk)
    else:
        form = AccommodationForm(instance=accommodation)
    return render(request, 'bookings/accommodation_form.html', {'form': form, 'title': 'Edit Accommodation'})

@user_passes_test(staff_required)
def accommodation_delete_view(request, pk):
    accommodation = get_object_or_404(Accommodation, pk=pk)
    if request.method == 'POST':
        accommodation.delete()
        messages.success(request, 'Accommodation deleted.')
        return redirect('bookings:accommodation_list')
    return render(request, 'bookings/accommodation_confirm_delete.html', {'accommodation': accommodation})

@login_required
def booking_create_view(request, accommodation_pk):
    accommodation = get_object_or_404(Accommodation, pk=accommodation_pk)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.accommodation = accommodation
            booking.total_amount = accommodation.price_per_night
            booking.save()
            messages.success(request, 'Booking created successfully!')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = BookingForm()
    return render(request, 'bookings/booking_form.html', {
        'form': form, 'accommodation': accommodation
    })

@login_required
def booking_detail_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    payments = booking.payments.all()
    return render(request, 'bookings/booking_detail.html', {
        'booking': booking, 'payments': payments
    })

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user).select_related('accommodation', 'guide').order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})

@login_required
def payment_create_view(request, booking_pk):
    booking = get_object_or_404(Booking, pk=booking_pk, user=request.user)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.booking = booking
            payment.amount = booking.total_amount
            payment.status = 'completed'
            payment.save()
            booking.status = 'confirmed'
            booking.save()
            messages.success(request, 'Payment successful! Booking confirmed.')
            return redirect('bookings:booking_detail', pk=booking.pk)
    else:
        form = PaymentForm()
    return render(request, 'bookings/payment_form.html', {'form': form, 'booking': booking})

@login_required
def booking_cancel_view(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        messages.info(request, 'Booking cancelled.')
        return redirect('bookings:my_bookings')
    return render(request, 'bookings/booking_cancel_confirm.html', {'booking': booking})
