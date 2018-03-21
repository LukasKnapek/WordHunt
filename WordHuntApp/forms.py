from django import forms
from WordHuntApp.models import *


class ImageUploadForm(forms.ModelForm):
    uploaded_image = forms.ImageField(label="Image")
    latitude = forms.DecimalField(label="Latitude in decimal degrees (optional)",
                                  max_digits=11,
                                  decimal_places=8,
                                  required=False)
    longitude = forms.DecimalField(label="Longitude in decimal degrees (optional)",
                                   max_digits=11,
                                   decimal_places=8,
                                   required=False)

    latitude.widget.attrs.update({'class': 'form-control',
                                  'id': 'latitude_field',
                                  'placeholder': 'e.g. 42.123456'})
    longitude.widget.attrs.update({'class': 'form-control',
                                   'id': 'longitude_field',
                                   'placeholder': 'e.g. -103.246801'})

    class Meta:
        model = Image
        exclude = ('related_word', 'user', 'avg_rating')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)
