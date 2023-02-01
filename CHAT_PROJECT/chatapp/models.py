from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    profile_picture = models.ImageField(blank=True,null=True)
    bio = models.TextField(blank=True,null=True)
    def __str__(self) -> str:
        return self.username


class UserChat(models.Model):
    user_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_from"
    )
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_to")

    def __str__(self) -> str:
        user = f"{self.user_from}               {self.user_to}"
        return user


class Chat(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    content = models.CharField(max_length=200, null=True, blank=True)
    users = models.ForeignKey(UserChat, on_delete=models.CASCADE, null=True, blank=True)
