from django.contrib import admin

# Register your models here.
from .models import Profile
from .models import Follow
from .models import Post
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Post)