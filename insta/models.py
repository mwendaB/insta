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

