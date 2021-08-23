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
                title=title, description=description, image_url=image_url)
            article.save()

            # create new auction with this article

            seller = request.user
            item = Article.objects.get(id=article.id)

            auction = AuctionList(seller=seller, item=item,
                                  price=price, article_category=article_category)
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


def auction_page(request, page):

    auction = AuctionList.objects.get(id=page)
    winner = Bid.objects.filter(auction=page).order_by('-price')[0].buyer

    # check if auction was created by actual user, if yes let him close it
    if str(auction.seller) == str(request.user.username):
        edit = True
    else:
        edit = None

    if request.method == "POST":

        # check if bid is higher than actual price
        if float(request.POST['bid']) > auction.price:

            # ad this bid to list of all bids for these auction
            bid = Bid(buyer=request.user, auction=auction,
                      price=float(request.POST['bid']))
            bid.save()

            # udpate price
            AuctionList.objects.filter(id=page).update(price=bid.price)
            auction = AuctionList.objects.get(id=page)

            message = f"You bid it with price {bid.price}!"

        else:

            message = "Bid must be higher than actual price!"

        # return page
        return render(request, "auctions/auction_page.html", {
            "auction": auction,
            "message": message,
            "edit": edit,
            "winner": winner

        })

    return render(request, "auctions/auction_page.html", {
        "auction": auction,
        "edit": edit,
        "winner": winner
    })


def delete(request):
    if request.method == "POST":

        # remove item and auction
        auction = AuctionList.objects.get(id=request.POST['auction'])
        item = Article.objects.get(title=auction.item)

        item.delete()
        auction.delete()

    return render(request, "auctions/index.html", {
        "auctions": AuctionList.objects.all()
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def categories_listing(request, category):
    return render(request, "auctions/index.html", {
        "auctions": AuctionList.objects.filter(article_category=category)
    })
