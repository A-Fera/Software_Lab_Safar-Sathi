from django import forms
from .models import Accommodation, Booking, Payment

W = {'class': 'form-control'}
S = {'class': 'form-select'}


class AccommodationForm(forms.ModelForm):
    """Photos handled via raw HTML input + request.FILES.getlist() in view."""

    class Meta:
        model = Accommodation
        fields = ['destination', 'name', 'accommodation_type', 'location', 'address',
                  'contact', 'phone', 'email', 'website', 'description', 'amenities',
                  'price_per_night', 'max_guests', 'check_in_time', 'check_out_time']
        widgets = {
            'destination': forms.Select(attrs=S),
            'accommodation_type': forms.Select(attrs=S),
            'name': forms.TextInput(attrs=W),
            'location': forms.TextInput(attrs=W),
            'address': forms.Textarea(attrs={**W, 'rows': 2}),
            'contact': forms.TextInput(attrs=W),
            'phone': forms.TextInput(attrs=W),
            'email': forms.EmailInput(attrs=W),
            'website': forms.URLInput(attrs=W),
            'description': forms.Textarea(attrs={**W, 'rows': 4}),
            'amenities': forms.Textarea(attrs={**W, 'rows': 3}),
            'price_per_night': forms.NumberInput(attrs=W),
            'max_guests': forms.NumberInput(attrs=W),
            'check_in_time': forms.TimeInput(attrs={**W, 'type': 'time'}),
            'check_out_time': forms.TimeInput(attrs={**W, 'type': 'time'}),
        }


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['guide']
        widgets = {
            'guide': forms.Select(attrs=S),
        }

    def __init__(self, *args, area_guides=None, **kwargs):
        super().__init__(*args, **kwargs)
        if area_guides is not None:
            self.fields['guide'].queryset = area_guides
        self.fields['guide'].required = False
        self.fields['guide'].empty_label = '-- No guide needed --'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['payment_method', 'transaction_id']
        widgets = {
            'payment_method': forms.Select(attrs=S),
            'transaction_id': forms.TextInput(
                attrs={**W, 'placeholder': 'Enter transaction ID (optional)'}),
        }
