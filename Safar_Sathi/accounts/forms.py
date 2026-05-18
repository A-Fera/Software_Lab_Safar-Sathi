from django import forms
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import CustomUser, LocalGuide

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Account', css_class='btn btn-primary w-100'))

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'language_preference', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Update Profile', css_class='btn btn-primary'))

class GuideForm(forms.ModelForm):
    user_first_name = forms.CharField(label='First Name')
    user_last_name = forms.CharField(label='Last Name')
    user_username = forms.CharField(label='Username')
    user_email = forms.EmailField(label='Email')

    class Meta:
        model = LocalGuide
        fields = ['region', 'description', 'experience_years', 'hourly_rate',
                  'languages', 'phone', 'guide_photo', 'references']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'references': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.instance_user = kwargs.pop('instance_user', None)
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['user_first_name'].initial = self.instance.user.first_name
            self.fields['user_last_name'].initial = self.instance.user.last_name
            self.fields['user_username'].initial = self.instance.user.username
            self.fields['user_email'].initial = self.instance.user.email
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
