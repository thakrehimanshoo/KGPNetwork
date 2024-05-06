from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'profile.html', {'form': form})


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
    return render(request, 'home.html')
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