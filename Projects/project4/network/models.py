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
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    followers=models.ManyToManyField(User, related_name='followers_list', default=None)
    following=models.ManyToManyField(User, related_name='following_list', default=None)

    def __str__(self):
        return f"{self.user}"

    def serialize(self):
        return{
            "id":self.id,
            "user":self.user.username,
            "followers":[user.username for user in self.followers.all()],
            "following":[user.username for user in self.following.all()],
            "followers_count":self.followers.count()
        }
