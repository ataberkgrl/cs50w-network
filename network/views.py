from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
import json


from .models import User, Post


def index(request):
    if request.method == "GET":
        posts = Post.objects.order_by("-datetime")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/index.html", {"page_obj": page_obj})
    if request.method == 'POST':
        if request.user.is_authenticated:
            post = Post.objects.create(content=request.POST["post"], posted_user=request.user)
            post.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return HttpResponseRedirect(reverse("login"))
    if request.method == "LIKE":
        data = json.loads(request.body)
        print(data)
        post = Post.objects.get(id=data["post_id"])
        user = User.objects.get(username=request.user.get_username())
        if post.liked_users.filter(username=request.user.get_username()).exists():
            post.liked_users.remove(user)
        else:
            post.liked_users.add(user)
        post.save()
        response = HttpResponse(status=204)
        response["like_count"] = post.liked_users.count()
        return response
    if request.method == "EDIT":
        data = json.loads(request.body)
        post = Post.objects.get(id=data["post_id"])
        if (post.posted_user == request.user):
            post.content = data["new_content"]
            post.save()
        response = HttpResponse(status=204)
        return response

def following(request):
    user = User.objects.get(username=request.user.get_username())
    following_users = user.follows.all()
    following_posts = (Post.objects.filter(posted_user__in=following_users).order_by("-datetime"))
    paginator = Paginator(following_posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {"page_obj": page_obj})

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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

def profile(request, username):
    if request.method == "GET":
        user = User.objects.get(username=username)
        is_followed = user.followers.filter(username=request.user.get_username()).exists()
        following_count = len(user.follows.all())
        followers_count = len(user.followers.all())
        posts = Post.objects.filter(posted_user=user).order_by("-datetime")
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        return render(request, "network/profile.html", {
            "page_obj": page_obj,
            "following_count": following_count,
            "followers_count": followers_count,
            "username": username,
            "is_followed": is_followed
        })
    if request.method == "FOLLOW":
        data = json.loads(request.body)
        follower = request.user
        followed = User.objects.get(username=data["followed_name"])
        response = HttpResponse(status=204)
        if follower in followed.followers.all():
            follower.follows.remove(followed)
            response["action"] = "unfollow"
        else:
            follower.follows.add(followed)
            response["action"] = "follow"
        return response

        



