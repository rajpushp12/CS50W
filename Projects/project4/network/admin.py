from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=("id","username","email", "last_login")

class PostAdmin(admin.ModelAdmin):
    list_display=("id","user","post_content","like_count","timestamp")

class ConnectionsAdmin(admin.ModelAdmin):
    list_display=("id","user")


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Connections, ConnectionsAdmin)
