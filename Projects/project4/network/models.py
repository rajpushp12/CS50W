from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):

    user=models.CharField(max_length=32)

    post_content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)
    like_count=models.IntegerField(default=0)

    def serialize(self):
        return{
            "id":self.id,
            "user":self.user,
            "post_content":self.post_content,
            "like_count":self.like_count
        }


class Connections(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='creator')
    followers=models.ManyToManyField(User, related_name='followers_list')
    following=models.ManyToManyField(User, related_name='following_list')

    def serialize(self):
        return{
            "id":self.id,
            "followers":self.followers,
            "floolwing":self.following
        }
