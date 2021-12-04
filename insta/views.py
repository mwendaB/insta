from django.shortcuts import render, redirect
from .forms import ProfileForm,ImageForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Image, Profile,Comments,Likes
from vote.managers import VotableManager

votes=VotableManager()

@login_required(login_url='/accounts/login/')
def index(request):
    current_user = request.user
    posts = Image.get_all_images()
    comments = Comments.objects.all()
    profile = Profile.get_all_profiles()
    
    
    return render(request, 'insta/index.html', locals())
    
@login_required(login_url='/accounts/login/')
def add_image(request):
        current_user = request.user
        if request.method == 'POST':
                form = ImageForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('index')
        else:
                form = ImageForm()
                return render(request,'insta/image.html', {"form":form})

@login_required(login_url='/accounts/login/')                
def profile_info(request):
        current_user = request.user
        profile = Profile.objects.filter(user=current_user).first()
        posts = request.user.image_set.all()
       
        return render(request, 'insta/profile.html', {"images": posts, "profile": profile})
@login_required(login_url='/accounts/login/') 
def profile_update(request):
         current_user = request.user
         if request.method == 'POST':
                form = ProfileForm(request.POST, request.FILES)
                if form.is_valid():
                        add=form.save(commit=False)
                        add.user = current_user
                        add.save()
                return redirect('profile')
         else:
                form = ProfileForm()
         return render(request,'insta/profile_update.html',{"form":form})

@login_required(login_url='/accounts/login/') 
def comment(request,image_id):
        current_user=request.user
        image = Image.objects.get(id=image_id)
        profile_owner = User.objects.get(username=current_user.username)
        comments = Comments.objects.all()
        
        if request.method == 'POST':
                form = CommentForm(request.POST, request.FILES)
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.image = image
                        comment.user = request.user
                        comment.save()
            
                       
                return redirect('index')
        else:
                form = CommentForm()
        return render(request, 'insta/comment.html',locals())


@login_required(login_url='/accounts/login/')
def search_results(request):
    if 'username' in request.GET and request.GET["username"]:
        search_term = request.GET.get("username")
        searched_users = User.objects.filter(username__icontains = search_term)
        message = f"{search_term}"
        profile_pic = User.objects.all()
        return render(request, 'insta/search.html', {'message':message, 'results':searched_users, 'profile_pic':profile_pic})
    else:
        message = "You haven't searched for any term"
        return render(request, 'insta/search.html', {'message':message})

def follow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.add_follower(request.user, other_user)

    return redirect('index')

def unfollow(request, user_id):
    other_user = User.objects.get(id = user_id)
    follow = Follow.objects.remove_follower(request.user, other_user)

    return redirect('index')

@login_required(login_url='/accounts/register/')
def like_images(request, id):
        image = Image.get_one_image(id)
        user = request.user
        user_id = user.id

        if user.is_authenticated:
                uplike = image.votes.up(user_id)
                image.like_add = image.votes.count()
                image.save()

        return redirect('index')
