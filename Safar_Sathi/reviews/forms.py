from django import forms
from .models import DestinationReview, AccommodationReview, GuideReview, ReviewPhoto

W = {'class': 'form-control'}
S = {'class': 'form-select'}
RATING_CHOICES = [(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)]


class DestinationReviewForm(forms.ModelForm):
    class Meta:
        model = DestinationReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Amazing experience!'}),
            'rating': forms.Select(attrs=S, choices=RATING_CHOICES),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'Share your experience...'}),
        }


class AccommodationReviewForm(forms.ModelForm):
    class Meta:
        model = AccommodationReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Great stay!'}),
            'rating': forms.Select(attrs=S, choices=RATING_CHOICES),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'Describe your stay...'}),
        }


class GuideReviewForm(forms.ModelForm):
    class Meta:
        model = GuideReview
        fields = ['title', 'rating', 'content']
        widgets = {
            'title': forms.TextInput(attrs={**W, 'placeholder': 'e.g. Very knowledgeable guide!'}),
            'rating': forms.Select(attrs=S, choices=RATING_CHOICES),
            'content': forms.Textarea(attrs={**W, 'rows': 5, 'placeholder': 'How was the guide?'}),
        }
