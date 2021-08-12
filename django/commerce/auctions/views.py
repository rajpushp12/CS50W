from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import *


def index(request):
    auction_list=Listing.objects.all()
    return render(request, "auctions/index.html", {
        "auction_list":auction_list
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create(request):
    if request.method == 'GET':
        return render(request, 'auctions/create.html')

    if request.method=='POST':

        item=Listing()
        item.title=request.POST.get("title")
        item.start_bid=int(request.POST.get("start_bid"))
        item.description=request.POST.get("description")
        item.category=request.POST.get("category")
        item.product_admin=request.user.username
        item.image_link=request.POST.get("image_link", "")

        item.save()
        return HttpResponseRedirect(reverse('index'))



@login_required(login_url='/login')
def listing(request, listing_id):
    check=Watchlist.objects.filter(user=request.user.username, listing_id=listing_id)
    current_bid=Bid.objects.filter(listing_id=listing_id)
    current_listing=Listing.objects.get(id=listing_id)
    comments=Comment.objects.filter(listing_id=listing_id)

    if request.method=='GET':

        if current_bid:
            return render(request, "auctions/listing.html", {
                "comments":comments,
                "current_listing":current_listing,
                "current_price":Bid.objects.get(listing_id=listing_id).bid,
                "check":check
            })

        else:
            return render(request, "auctions/listing.html", {
                "comments":comments,
                "current_listing":current_listing,
                "current_price":current_listing.start_bid,
                "check":check
            })


    if request.method=='POST':

        bid=int(request.POST["bid"])

        if current_bid:

            currentbid=Bid.objects.get(listing_id=listing_id)

            if bid>currentbid.bid:
                currentbid.bid=bid
                currentbid.user=request.user.username
                currentbid.save()

                return render(request, "auctions/listing.html", {
                    "comments":comments,
                    "current_listing":current_listing,
                    "check":check,
                    "current_price":currentbid.bid,
                    "message":"YOUR BID HAS BEEN PLACED SUCCESSFULLY"
                })

            else:

                return render(request, "auctions/listing.html", {
                    "comments":comments,
                    "current_listing":current_listing,
                    "check":check,
                    "current_price":currentbid.bid,
                    "message":"BID SHOULD BE GREATER THAN THE CURRENT BID"
                })


        else:

            if bid>current_listing.start_bid:

                item=Bid()
                item.bid=bid
                item.listing_id=listing_id
                item.user=request.user.username
                item.save()

                return render(request, "auctions/listing.html", {
                    "comments":comments,
                    "current_listing":current_listing,
                    "check":check,
                    "current_price":bid,
                    "message":"YOUR BID HAS BEEN PLACED SUCCESSFULLY"
                })


            else:

                return render(request, "auctions/listing.html", {
                    "comments":comments,
                    "current_listing":current_listing,
                    "check":check,
                    "current_price":current_listing.start_bid,
                    "message":"BID SHOULD BE GREATER THAN THE STARTING BID"
                })



@login_required(login_url='/login')
def categories(request):

    return render(request, "auctions/categories.html")


@login_required(login_url='/login')
def category(request, cat):

    details=Listing.objects.filter(category=cat)
    return render(request, "auctions/category.html", {
        "details":details,
        "category":cat
    })




@login_required(login_url='/login')
def watch(request, product_id):

    watch=Watchlist.objects.filter(listing_id=product_id, user=request.user.username)
    
    if watch:
        watch.delete()

    else:
        watch=Watchlist()
        watch.user=request.user.username
        watch.listing_id=product_id
        watch.save()

    return redirect('listing', product_id)


@login_required(login_url='/login')
def watchlist(request):

    watch=Watchlist.objects.filter(user=request.user.username)

    if watch:

        items=[]

        for i in watch:
            items.append(Listing.objects.get(id=i.listing_id))

        return render(request, "auctions/watchlist.html", {
            "items":items
        })

    else:
        return render(request, "auctions/watchlist.html", {
            "message":"There are no items in the watchlist."
        })



@login_required(login_url='/login')
def closebid(request, listing_id):

    item=Listing.objects.get(id=listing_id)
    watchlist_detail=Watchlist.objects.filter(listing_id=listing_id)
    comment_detail=Comment.objects.filter(listing_id=listing_id)
    bid_detail=Bid.objects.get(listing_id=listing_id)

    winner=Winner()

    winner.winning_bid=bid_detail.bid
    winner.listing_id=item.id
    winner.user=bid_detail.user
    winner.title=item.title
    winner.save()

    item.delete()
    bid_detail.delete()

    if watchlist_detail:
        watchlist_detail.delete()

    if comment_detail:
        comment_detail.delete()

    return redirect('index')



@login_required(login_url='/login')
def closedlisting(request):

    winner_list=Winner.objects.filter(user=request.user.username)


    if winner_list:
        return render(request, 'auctions/closedlisting.html', {
            "winner_list":winner_list
        })

    else:
        return render(request, 'auctions/closedlisting.html', {
            "message":"YOU STILL HAVE NO WINNINGS, COME BACK IN A WHILE!"
        })

    

@login_required(login_url='/login')
def comment(request, listing_id):

    add_comment=Comment()
    add_comment.listing_id=listing_id
    add_comment.user=request.user.username
    add_comment.comment=request.POST.get("comment","")

    add_comment.save()

    return redirect('listing', listing_id)









