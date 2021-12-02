from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import *


# Create your views here.
@login_required(login_url='/accounts/login/')
def home(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

