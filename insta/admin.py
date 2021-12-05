from django.contrib import admin
from .models import Image, Profile, Category, Comments

# Register your models here.
class ImageAdmin(admin.ModelAdmin):
    filter_horizontal = ('category',)

admin.site.register(Image, ImageAdmin)
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Comments)