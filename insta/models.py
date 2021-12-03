from django.db import models
import datetime as dt
from django.contrib.auth.models import User
from django.db.models.fields import related
from cloudinary.models import CloudinaryField

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(
    User, on_delete=models.CASCADE, related_name='images')
    image=CloudinaryField('image')
    image_name = models.CharField(max_length=50)
    image_caption = models.TextField()
    posted_on = models.DateTimeField(auto_now_add=True)
    profile = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)


    class Meta:
        ordering = ['-posted_on']
    

    @classmethod
    def get_images_by_user(cls, user):
        posts = cls.objects.filter(user=user)
        return posts
    def delete_image(self):
        self.delete()
    
    @classmethod
    def get_all_comments(self):
        return self.objects.comments.all()

    def save_image(self):
        self.save()
    
    def update_caption(self, new_caption):
        self.image_caption = new_caption
        self.save()

    @classmethod
    def search_by_image_name(cls, search_term):
        posts = cls.objects.filter(
            image_name__icontains=search_term)
        return posts

    def __str__(self):
        return self.image_name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo=CloudinaryField('image')
    bio = models.TextField(max_length=500, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)

    def update(self):
        self.save()

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profile_by_user(cls, user):
        profile = cls.objects.filter(user=user)
        return profile

    def __str__(self):
        return self.user.username


