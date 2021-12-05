from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from .models import Image, Profile
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, ImageUploadForm

from .email import send_welcome_email

# Create your views here.
@login_required(login_url='/accounts/login')
def home(request):
    latest_pics = Image.objects.order_by('-id').select_related('profile').all()
    current_user = request.user
    profile = Profile.objects.get(user = current_user.id)

    current_user = request.user

    return render(request, 'home.html', {"latest_pics": latest_pics, "current_user": current_user, "profile": profile})

@login_required(login_url='/accounts/login')
def profile(request, user_id):
    imgs = Image.objects.filter(profile = user_id)
    current_user = request.user
    profile = Profile.objects.get(user = user_id)

    return render(request, 'profile.html', {"current_user": current_user, "imgs": imgs, "profile": profile})

@login_required(login_url='/accounts/login')
def profile_update(request, user_id):

    title = 'Update Profile'
    profile = Profile.objects.get(user = user_id)

    current_user = request.user

    email = current_user.email

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            fname = form.cleaned_data['first_name']
            lname = form.cleaned_data['last_name']
            about = form.cleaned_data['bio']
            mobile = form.cleaned_data['phone_number']
            dp = form.cleaned_data['profile_photo']

            # Profile.objects.filter(pk=current_user.id).save(first_name = fname, last_name = lname, email = current_user.email, bio = about, phone_number = mobile, prof_photo = dp)

            # profile = Profile.objects.filter(pk=current_user.id).update(first_name = fname, last_name = lname, email = current_user.email, bio = about, phone_number = mobile, prof_photo = dp)
            
            Profile.objects.filter(user = request.user).update(first_name = fname, last_name = lname, email = current_user.email, bio = about, phone_number = mobile, prof_photo = dp)

            return redirect(home)

    else:
        form = ProfileForm()
    
    return render(request, 'profile_update.html', {"ProfileForm": form, "title": title, "profile": profile})

@login_required(login_url='/accounts/login')
def image_uploader(request, user_id):

    current_user = request.user
    profile = Profile.objects.get(user = current_user.id)

    prof_user = Profile.objects.get(user=user_id)

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data['image']
            i_name = form.cleaned_data['image_name']
            i_caption = form.cleaned_data['image_caption']
            tags = form.cleaned_data['category']

            image = Image(image = img, img_name = i_name, img_caption = i_caption, profile = prof_user, likes = 0)
            image.save()

            # image.category.add(tags)

            return redirect(home)
    else:
        form = ImageUploadForm()
    
    return render(request, 'image_upload.html', {"ImageUploadForm": form, "profile": profile})

def likes(request, pic_id):
    img = Image.objects.get(id = pic_id)
    new_likes = img.likes + 1

    # img.update(likes = new_likes)
    Image.objects.filter(pk=pic_id).update(likes = new_likes)

    return redirect(home)

def index_test(request):
    title = "ingram index page testpage"

    return render(request, 'index.html', {"title": title})