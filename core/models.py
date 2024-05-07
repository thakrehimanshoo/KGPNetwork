from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', default='static/profile_pics/user_icon.jpg', blank=True)

    def __str__(self):
        return self.user.username
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=240, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Post by {self.author.username} at {self.created_at}'
