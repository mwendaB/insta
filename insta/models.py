from django.db import models

# Signals
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, blank=True, default=0000, on_delete=models.CASCADE)
    first_name = models.CharField(max_length = 30)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField()
    bio = models.TextField()
    phone_number = models.CharField(max_length =15, blank = True)
    prof_photo = models.ImageField(upload_to = 'pics/profiles/')

    def __str__(self):
        return self.first_name
    
    def save_profile(self):
        self.save()
    
    def delete_profile(self):
        self.delete()
    
    def update_profile(self):
        pass
    
    
    @receiver(post_save, sender=User)
    def create_or_update_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
    
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Category(models.Model):
    tag = models.CharField(max_length = 30)

    def __str__(self):
        return self.tag

class Comments(models.Model):
    comment = models.CharField(max_length = 500)

    def __str__(self):
        return self.comment

class Image(models.Model):
    image = models.ImageField(upload_to = 'pics/')
    img_name = models.CharField(max_length = 150)
    img_caption = models.CharField(max_length = 1000)
    profile = models.ForeignKey(Profile , on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField()
    comments = models.ManyToManyField(Comments, blank=True)

    def __str__(self):
        return self.img_name
    
    def save_image(self):
        self.save()
    
    def delete_image(self):
        self.delete()
    
    def update_image(self):
        pass
