from django import forms
from .models import Itinerary, ItineraryItem

W = {'class': 'form-control'}
S = {'class': 'form-select'}

class ItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['name', 'description', 'start_date', 'end_date', 'status', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Sundarbans Weekend Trip'}),
            'description': forms.Textarea(attrs={**W, 'rows': 3}),
            'start_date': forms.DateInput(attrs={**W, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={**W, 'type': 'date'}),
            'status': forms.Select(attrs=S),
        }

class ItineraryItemForm(forms.ModelForm):
    class Meta:
        model = ItineraryItem
        fields = ['title', 'item_type', 'destination', 'accommodation', 'start_date', 'end_date', 'estimated_cost', 'notes']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'Activity title'}),
            'item_type': forms.Select(attrs=S),
            'destination': forms.Select(attrs=S),
            'accommodation': forms.Select(attrs=S),
            'start_date': forms.DateInput(attrs={**W, 'type': 'date'}),
            'end_date': forms.DateInput(attrs={**W, 'type': 'date'}),
            'estimated_cost': forms.NumberInput(attrs=W),
            'notes': forms.Textarea(attrs={**W, 'rows': 3, 'placeholder': 'Optional notes...'}),
        }
