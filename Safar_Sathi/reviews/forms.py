from django import forms
from .models import DestinationReview, AccommodationReview, GuideReview

W = {'class': 'form-control'}
S = {'class': 'form-select'}

class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'Review title'}),
            'rating': forms.Select(attrs=S, choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'Share your experience...'}),
        }

class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'Review title'}),
            'rating': forms.Select(attrs=S, choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'Share your experience...'}),
        }

class GuideReviewForm(forms.ModelForm):
    class Meta:
        model = GuideReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'Review title'}),
            'rating': forms.Select(attrs=S, choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'How was the guide?'}),
        }
