from typing import Text
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        # print only active auctions
        "auctions": AuctionList.objects.filter(active=True),
        "title": "Active Listings"
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
        try:
            article_category = Category.objects.get(
                type=request.POST["category"])
        except:
            article_category = None

        # if user not provide photo please set defalt photo
        if not image_url:
            image_url = "http://www.clker.com/cliparts/B/u/S/l/W/l/no-photo-available-md.png"

        if title and description and price and article_category:

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

    # define auction
    auction = AuctionList.objects.get(id=page)

    if auction.active == True:

        message = ""

        # check if auction was created by actual user, if yes let him close it
        if str(auction.seller) == str(request.user.username):
            edit = True
        else:
            edit = None

        if request.method == "POST":

            # watchlist button
            if "watchlist" in request.POST:
                action = request.POST["action"]

            # check if user already have watchlist, if not create one
                try:
                    watchlist = Watchlist.objects.get(user=request.user)

                    if action == "add":
                        watchlist.auction.add(auction)
                    elif action == "remove":
                        watchlist.auction.remove(auction)
                except:
                    new_watchlist = Watchlist(user=request.user)
                    new_watchlist.save()

                    watchlist = Watchlist.objects.get(user=request.user)
                    watchlist.auction.add(auction)

            # bid button
            if "bid" in request.POST:
                if request.POST['bid_value']:
                    # check if bid is higher than actual price
                    if float(request.POST['bid_value']) > auction.price:

                        # ad this bid to list of all bids for these auction
                        bid = Bid(buyer=request.user, auction=auction,
                                  price=float(request.POST['bid_value']))
                        bid.save()

                        # udpate price
                        AuctionList.objects.filter(
                            id=page).update(price=bid.price)

                        # update winner
                        winner = Bid.objects.filter(
                            auction=page).order_by('-price')[0].buyer
                        AuctionList.objects.filter(
                            id=page).update(winner=winner)

                        # udpate auction
                        auction = AuctionList.objects.get(id=page)

                        message = f"You bid it with price {bid.price}!"

                    else:

                        message = "Bid must be higher than actual price!"

            # delete button
            if "delete" in request.POST:
                # set status of the auction as inactive

                AuctionList.objects.filter(id=page).update(active=False)

                # set the actual winner (higher bid from bids table)
                try:
                    winner = Bid.objects.filter(
                        auction=page).order_by('-price')[0].buyer
                    AuctionList.objects.filter(id=page).update(winner=winner)
                except:
                    winner = ""

                # redirect to start page
                return HttpResponseRedirect(reverse("index"))

            # comment button
            if "comment" in request.POST:
                comment_text = request.POST["text"]

                if comment_text:
                    comment = Comment(author=request.user,
                                      auction_comment=auction, text=comment_text)
                    comment.save()

        # check if item is on user watchlist
        user_watchlist = []
        try:
            for id in (Watchlist.objects.get(user=request.user.id)).auction.all():
                user_watchlist.append(id.id)

            if int(page) in user_watchlist:
                watchlist = True
            else:
                watchlist = False
        except:
            watchlist = False

        # set the actual winner (higher bid from bids table)
        try:
            winner = Bid.objects.filter(
                auction=page).order_by('-price')[0].buyer
            AuctionList.objects.filter(id=page).update(winner=winner)
        except:
            winner = ""

        # comments for this auction

        try:
            comments = Comment.objects.filter(auction_comment=page)
        except:
            comments = ""

        # return page
        return render(request, "auctions/auction_page.html", {
            "auction": auction,
            "message": message,
            "edit": edit,
            "watchlist": watchlist,
            "comments": comments

        })

    else:
        return render(request, "auctions/history.html", {
            "auction": auction
        })


def watchlist(request):
    try:
        watchlist = (Watchlist.objects.get(user=request.user.id))
        watchlist_auction = watchlist.auction.filter(active=True)
    except:
        watchlist_auction = ""

    return render(request, "auctions/index.html", {
        "auctions": watchlist_auction,
        "title": "Watchlist"
    })


def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })


def categories_listing(request, category):

    # set the page title on category name
    title = Category.objects.get(id=category)

    return render(request, "auctions/index.html", {
        "auctions": AuctionList.objects.filter(article_category=category, active=True),
        "title": title.type
    })


def user_panel(request):

    # find all auctions bided by actuall user
    user_bid = set()

    auctions = Bid.objects.filter(buyer=request.user.id)

    for auction in auctions:
        user_bid.add(auction.auction)

    return render(request, "auctions/userpanel.html", {
        "auctions": user_bid,
    })
