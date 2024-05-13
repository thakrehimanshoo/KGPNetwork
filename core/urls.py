from django.urls import path, include
from core import views
from . import views as view

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('signup/', views.user_signup, name='register'),
    path('profile/', views.profile, name='profile'),
    path('userprofile/<str:userid>/', views.user_profile, name='user_profile'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('following/', views.following_list, name='following_list'),
    path('createpost/', views.create_post, name='create_post'),
    path('posts/', views.posts, name='posts'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('editprofile/', views.edit_profile, name='edit_profile'),
    
]