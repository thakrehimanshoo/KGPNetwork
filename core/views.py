from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def login(request):
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