from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    profile_pic = None  # Default value for profile_pic
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
        # Check if profile picture exists before accessing URL
        if request.user.profile.profile_picture:
            profile_pic = request.user.profile.profile_picture.url

    # Pass context as a single dictionary
    return render(request, 'profile.html', {'form': form, 'profile_pic': profile_pic})


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
def login(request):
        if request.user.is_authenticated:
           return redirect('/')

        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:  
                return render(request, 'login.html', {'error': True})
        return render(request, 'login.html')        
def home(request):
    if request.user.is_anonymous:
        return redirect('/login/')
    users = User.objects.all()
    return render(request, 'home.html',{'users': users})
def logout(request):
    auth_logout(request)
    return redirect('/login/')
def user_signup(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            form = SignupForm()
            return render(request, 'signup.html', {'form': form, 'error': True})
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def user_profile(request, userid):
    # return HttpResponse(f'User Profile of {username}')
    user = User.objects.get(username=userid)
    return render(request, 'user_profile.html', {'user': user})