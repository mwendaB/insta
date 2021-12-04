from django.contrib import admin
from .models import Image, Profile, Comments

admin.site.register(Profile)
admin.site.register(Image)
admin.site.register(Comments)