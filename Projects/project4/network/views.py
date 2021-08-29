import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "network/index.html",{
        "posts":Post.objects.all().order_by('-timestamp')
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")



def create_post(request):
    if request.method == "GET":
        return render(request, 'network/create.html')

    if request.method == "POST":

        item=Post()
        item.post_content=request.POST['post_content']
        item.user=request.user.username
        item.save()

        return HttpResponseRedirect(reverse('index'))


def profile(request, username):
    if request.method=='GET':

        user=User.objects.get(username=username)
        posts=Post.objects.filter(user=username).order_by('timestamp')

        try:
            list=Connections.objects.get(user=user.id)

            if username==user.username:
                return render(request, 'network/profile.html',{
                    "profile_user":username,
                    "posts":posts,
                    "follower_count":list.followers.all().count(),
                    "following_count":list.following.all().count(),
                    "status":True
                })

            else:
                return render(request, 'network/profile.html',{
                    "profile_user":username,
                    "posts":posts,
                    "follower_count":list.followers.all().count(),
                    "following_count":list.following.all().count()
                })

        except Connections.DoesNotExist:
            return render(request, 'network/profile.html',{
                    "profile_user":username,
                    "posts":posts,
                    "follower_count":0,
                    "following_count":0
                })

@login_required
def connections(request, username):
    if request.method=='GET':

        user=User.objects.get(username=username)
        try:
            list=Connections.objects.get(user=user.id)
            content_list=list.following.all()
            l1=[]

            for creator in content_list:
                posts=Post.objects.filter(user=creator)
                for post in posts:
                    l1.append(post)

            return render(request, "network/index.html",{
                "posts":l1
            })

        except Connections.DoesNotExist:
            return HttpResponse("Error code: 404")

   


