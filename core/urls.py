from django.urls import path, include
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.user_signup, name='register'),
    path('profile/', views.profile, name='profile'),
]