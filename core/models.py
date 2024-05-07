from django.db import models
from django.contrib.auth.models import User
from PIL import Image
import os
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='static/profile_pics/', default='static/profile_pics/user_icon.jpg', blank=True)

    def __str__(self):
        return self.user.username
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        if self.profile_picture:
            
            img = Image.open(self.profile_picture)
            if img.mode != 'RGB':
                img = img.convert('RGB')

            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path, format='JPEG')

            


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
