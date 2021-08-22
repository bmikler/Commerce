from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": AuctionList.objects.all()
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


def create_listing(request):
    if request.method == "POST":

        # create article for auction
        title = request.POST["title"]
        description = request.POST["description"]
        image_url = request.POST["url"]
        price = request.POST["price"]
        article_category = Category.objects.get(type=request.POST["category"])

        # if user not provide photo please set defalt photo
        if not image_url:
            image_url = "http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png"

        if title and description and price:

            article = Article(
                title=title, description=description, image_url=image_url, article_category=article_category)
            article.save()

            # create new auction with this article

            seller = request.user
            item = Article.objects.get(id=article.id)

            auction = AuctionList(seller=seller, item=item, price=price)
            auction.save()

            # redirect to main mage
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "auctions/create_listing.html", {
                "message": "Please fill all fields.",
                "categories": Category.objects.all()
            })

    return render(request, "auctions/create_listing.html", {
        "categories": Category.objects.all()
    })
