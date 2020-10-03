from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    follows = models.ManyToManyField("self", symmetrical=False, related_name="followers")

class Post(models.Model):
    content = models.CharField(max_length=280)
    datetime = models.DateTimeField(auto_now_add=True)
    posted_user = models.ForeignKey("User", on_delete=models.CASCADE)
    liked_users = models.ManyToManyField("User", symmetrical=False, related_name="liked_posts")