from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title=models.CharField(max_length=16)
    start_bid=models.IntegerField()
    description=models.TextField()
    category=models.CharField(max_length=64)
    product_admin=models.CharField(max_length=32)
    image_link = models.TextField(default=None, blank=True)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    bid=models.IntegerField()
    listing_id=models.IntegerField()
    user=models.CharField(max_length=32)

    def __str__(self):
        return f"{self.bid}"

class Watchlist(models.Model):
    listing_id=models.IntegerField()
    user=models.CharField(max_length=32)


class Comment(models.Model):
    listing_id=models.IntegerField()
    user=models.CharField(max_length=32)
    comment=models.TextField(default=None, blank=True)


class Winner(models.Model):
    winning_bid=models.IntegerField()
    listing_id=models.IntegerField()
    title=models.CharField(max_length=16)
    user=models.CharField(max_length=32)

    def __str__(self):
        return f"{self.title} {self.user} {self.winning_bid}"