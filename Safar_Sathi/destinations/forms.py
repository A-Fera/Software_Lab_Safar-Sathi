from django import forms
from .models import Destination, Photo, DIVISION_CHOICES

W = {'class': 'form-control'}
S = {'class': 'form-select'}


class DestinationForm(forms.ModelForm):
    """No photo field here — photos are handled via raw HTML input + request.FILES.getlist() in the view."""

    class Meta:
        model = Destination
        fields = ['name', 'description', 'location', 'division', 'country',
                  'category', 'best_time_to_visit', 'entry_fee', 'is_featured']
        widgets = {
            'name': forms.TextInput(attrs=W),
            'description': forms.Textarea(attrs={**W, 'rows': 5}),
            'location': forms.TextInput(attrs=W),
            'division': forms.Select(attrs=S,
                choices=[('', 'Select Division')] + list(DIVISION_CHOICES)),
            'country': forms.TextInput(attrs=W),
            'category': forms.Select(attrs=S),
            'best_time_to_visit': forms.TextInput(attrs=W),
            'entry_fee': forms.NumberInput(attrs=W),
        }


class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['image', 'caption']
        widgets = {
            'image': forms.FileInput(attrs={**W, 'accept': 'image/*'}),
            'caption': forms.TextInput(attrs={**W, 'placeholder': 'Optional caption'}),
        }
