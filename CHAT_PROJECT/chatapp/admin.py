from django.contrib import admin
from chatapp.models import Chat,User,UserChat
from django.contrib.auth.admin import UserAdmin

# Register your models here.


admin.site.register(Chat)
admin.site.register(UserChat)
admin.site.register(User)

