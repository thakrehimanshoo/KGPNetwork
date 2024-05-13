from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from .models import Post
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

# class editprofile(forms.ModelForm):
#     new_username = forms.CharField(max_length=150, required=False, label='New Username')

#     class Meta:
#         model = User
#         fields = ['new_username']

#     def __init__(self, *args, **kwargs):
#         self.user = kwargs.pop('user')
#         super().__init__(*args, **kwargs)
#         self.password_change_form = PasswordChangeForm(user=self.user, data=None)

#     def clean(self):
#         cleaned_data = super().clean()
#         new_username = cleaned_data.get('new_username')
#         password_form = self.password_change_form

#         if new_username:
#             self.user.username = new_username
#             self.user.save()

#         if password_form.is_valid():
#             password_form.save(commit=False)
#             self.user.set_password(password_form.cleaned_data['new_password1'])
#             self.user.save()

#         return cleaned_data

class SignupForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']

