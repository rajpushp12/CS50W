from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):

    user=models.CharField(max_length=32)

    post_content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    like_count=models.IntegerField(default=0)


class Connections(models.Model):
    followers=models.ManyToManyField(User, related_name='user_follower_list')
    following=models.ManyToManyField(User, related_name='user_following_list')
