from django import forms
from .models import Accommodation, Booking, Payment

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = ['destination', 'name', 'accommodation_type', 'location', 'address',
                  'contact', 'phone', 'email', 'website', 'description', 'amenities',
                  'price_per_night', 'max_guests', 'check_in_time', 'check_out_time', 'image']
        widgets = {
            'check_in_time': forms.TimeInput(attrs={'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 2}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guide']
        widgets = {
            'guide': forms.Select(attrs={'class': 'form-select'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'transaction_id': forms.TextInput(attrs={'placeholder': 'Enter transaction ID (optional)'}),
        }
