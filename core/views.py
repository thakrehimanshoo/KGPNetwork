from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .forms import SignupForm
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Follow
from .models import Post
from .forms import PostForm



# from .forms import editprofile
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')  # Redirect to home or wherever you want after posting
    else:
        form = PostForm()
    return redirect('home')

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    # Check if the user is not already followed
    if not request.user.following.filter(following=user_to_follow).exists():
        # Create a new Follow object to represent the follow relationship
        follow_object = Follow(follower=request.user, following=user_to_follow)
        follow_object.save()
    source = request.GET.get('source')
    if source == 'suggestion':
        return redirect('suggestion')
    else:
        return redirect('home')


@login_required
def unfollow_user(request, username):
    followed_user = User.objects.get(username=username)
    follow_instance = Follow.objects.filter(follower=request.user, following=followed_user).first()
    if follow_instance:
        follow_instance.delete()
        # Unfollow relationship deleted successfully
        # You can add a success message here if needed
    else:
        # Follow relationship does not exist
        # You can add a message indicating this if needed
        pass
    return redirect('following_list')



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
            print(user) 
            if user is not None:
                auth_login(request, user)
                return redirect('/')
            else:  
                return render(request, 'login.html', {'error': True})
        return render(request, 'login.html')        
def home(request):
    if request.user.is_anonymous:
        return redirect('/login/')
    
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)


    users = User.objects.exclude(id__in=following_ids)
    if users.count() == True:
        emptyval = True
    else:    
        emptyval = False

    # following_id = request.user.following.values_list('id', flat=True)
    posts = Post.objects.filter(author_id__in=following_ids).order_by('-created_at')
    myposts = Post.objects.filter(author_id=request.user.id).order_by('-created_at')
    combined_posts = (posts | myposts).order_by('-created_at')
    if combined_posts.count()== 0:
        postval = True 
    else:
        postval = False
    
    return render(request, 'home.html',{'users': users, 'thisuser': request.user, 'emptyval': emptyval, 'posts': combined_posts,  'postval': postval})

def posts(request):
    posts = Post.objects.filter(author_id=request.user.id).order_by('-created_at')
    if posts.count() == 0:
        postval = True
    else:
        postval = False
    return render(request, 'posts.html', {'posts': posts, 'postval': postval})

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

@login_required
def following_list(request):
    # Retrieve the logged-in user object
    user = request.user
    
    # Query all Follow objects where the following field matches the logged-in user
    followings = Follow.objects.filter(follower=user)
    if followings.count() == 0:
        emptyval = True
    else:  
        emptyval = False
    return render(request, 'following.html', {'followings': followings, 'emptyval': emptyval})

def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    # Check if the current user is the author of the post
    if request.user == post.author:
        post.delete()
        # Optionally, redirect the user to a different page after deletion
        return redirect('posts')
    else:
        # Handle unauthorized deletion (e.g., show an error message)
        return redirect('posts')  # Redirect back to the home page
def suggestion(request):
    following_ids = Follow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    users = User.objects.exclude(id__in=following_ids)
    if users.count() == True:
        emptyval = True
    else:    
        emptyval = False
    return render(request, 'suggestion.html', {'users': users, 'emptyval': emptyval})





from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages


from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm

def edit_profile(request):
    profile_pic = None
    if request.user.profile.profile_picture:
        profile_pic = request.user.profile.profile_picture.url

    if request.method == 'POST':
        if request.user.has_usable_password():
            
            form = PasswordChangeForm(request.user, request.POST)
        else:
            
            form = SetPasswordForm(request.user, request.POST)
            
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        if request.user.has_usable_password():
            form = PasswordChangeForm(request.user)
        else:
            form = SetPasswordForm(request.user)

    return render(request, 'editprofile.html', {
        'form': form,
        'profile_pic': profile_pic
    })

# @login_required
# def edit_profile(request):
#     if request.user.profile.profile_picture:
#             profile_pic = request.user.profile.profile_picture.url
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('edit_profile')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'editprofile.html', {
#         'form': form,
#         'profile_pic': profile_pic
#     })

# class CustomPasswordChangeForm(PasswordChangeForm):
#     def __init__(self, *args, **kwargs):
#         super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
#         if not self.user.has_usable_password():
#             self.fields['old_password'].widget.attrs['readonly'] = True
#             self.fields['old_password'].help_text = "You haven't set a password yet. Please set a new password."