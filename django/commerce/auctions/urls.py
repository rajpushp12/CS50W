from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watch/<int:product_id>", views.watch, name="watch"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cat>", views.category, name="category"),
    path("closebid/<int:listing_id>", views.closebid, name="closebid"),
    path("closedlisting", views.closedlisting, name="closedlisting"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
]
