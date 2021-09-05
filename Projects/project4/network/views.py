import json
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *


def index(request):

    posts=Post.objects.all().order_by('-timestamp')
    paginator=Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html",{
        "posts":page_obj
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

            connection=Connections()
            connection.user=user
            connection.save()

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

    if request.user.is_authenticated:
        user=User.objects.get(username=username)
        posts=Post.objects.filter(user=username).order_by('-timestamp')

        paginator=Paginator(posts, 10)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        list=Connections.objects.get(user=user.id)

        return render(request, 'network/profile.html',{
                "name":username,
                "posts":page_obj,
                "follower_count":list.followers.count(),
                "following_count":list.following.count()
            })

    else:
        return HttpResponseRedirect(reverse('login'))


@login_required
@csrf_exempt
def connect_fetch(request, username):

    user=User.objects.get(username=username)
    list=Connections.objects.get(user=user.id)
        
    return JsonResponse(list.serialize())



@login_required
@csrf_exempt
def connect_add(request, username):

    user=User.objects.get(username=username)
    
    list=Connections.objects.get(user=user.id)
    list1=Connections.objects.get(user=request.user.id)
        
    
    if request.method=='PUT':

        list.followers.add(request.user)
        list1.following.add(user)


@login_required
@csrf_exempt
def connect_remove(request, username):

    user=User.objects.get(username=username)
    
    list=Connections.objects.get(user=user.id)
    list1=Connections.objects.get(user=request.user.id)

    if request.method=='PUT':

        list.followers.remove(request.user)
        list1.following.remove(user)






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

            paginator=Paginator(l1, 10)

            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            return render(request, "network/index.html",{
                "posts":page_obj
            })

        except Connections.DoesNotExist:
            return HttpResponse("Error code: 404")


@csrf_exempt
def post(request,id):

    #Query for requested email
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method=='GET':
        return JsonResponse(post.serialize())

    if request.method == 'PUT':
        data = json.loads(request.body)

        post.post_content=data["post_content"]
        post.save()



@csrf_exempt
def like(request,id):

    #Query for requested email
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

    if request.method=='GET':
        return JsonResponse(post.serialize())

    if request.method == 'PUT':
        data = json.loads(request.body)

        post.like_count=data["like_count"]
        post.save()