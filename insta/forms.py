from django import forms
from .models import Profile

class ProfileForm(forms.Form):
    first_name = forms.CharField(label = 'First Name:', max_length=30)
    last_name = forms.CharField(label = 'Last Name:', max_length=30, required=False)
    bio = forms.CharField(label = "About You:", widget=forms.Textarea)
    phone_number = forms.IntegerField(label = "Phone Number:")
    profile_photo = forms.ImageField(label = "Profile Photo:")

class ImageUploadForm(forms.Form):
    image = forms.ImageField(label = "Image:")
    image_name = forms.CharField(label = "Image Name:", max_length=50)
    image_caption = forms.CharField(label = "Image Caption:", max_length=300)
    category = forms.CharField(label = "Category:", max_length=100)


