from django.contrib import admin
from .models import *
# Register your models here.


class ListingAdmin(admin.ModelAdmin):
	list_display=("id","title","product_admin","start_bid","description", "image_link")

class WatchlistAdmin(admin.ModelAdmin):
	list_display=("listing_id","user")

class BidAdmin(admin.ModelAdmin):
	list_display=("listing_id","user","bid")

class WinnerAdmin(admin.ModelAdmin):
	list_display=("listing_id","title","user","winning_bid")

class CommentAdmin(admin.ModelAdmin):
	list_display=("listing_id","user","comment")

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Watchlist, WatchlistAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Winner, WinnerAdmin)