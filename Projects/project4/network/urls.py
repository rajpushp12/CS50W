from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name="create"),
    path("<str:username>", views.profile, name="profile"),
    path("<str:username>/connections", views.connections, name="connections"),

    #API Routes
    path("post/<int:id>", views.post, name="post")
]
