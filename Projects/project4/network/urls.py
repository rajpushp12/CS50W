from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("<str:username>/connections", views.connections, name="connections"),

    #API Routes
    path("post/<int:id>", views.post, name="post"),
    path("like/<int:id>", views.like, name="like"),
    path("connect_fetch/<str:username>", views.connect_fetch, name="connect_fetch"),
    path("connect_add/<str:username>", views.connect_add, name="connect_add"),
    path("connect_remove/<str:username>", views.connect_remove, name="connect_remove")
]
