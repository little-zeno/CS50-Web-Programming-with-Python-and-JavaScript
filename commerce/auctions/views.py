# views.py

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError, models
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listings, Bids, Comments
from django.views.generic.edit import CreateView

from .forms import CreateForm, CommentForm, BidForm
from django.db.models import Max, Count
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError





def index(request):
    active_listings = Listings.objects.filter(active=True).annotate(highest_bid=Max('bids__bid_price'))
    return render(request, "auctions/index.html", {"active_listings": active_listings})


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

@login_required
def create(request):
    if request.method == "POST":
        new_form = CreateForm(request.POST)
        if new_form.is_valid():
            new_title = new_form.cleaned_data["title"]
            new_description = new_form.cleaned_data["description"]
            new_price = new_form.cleaned_data["price"]
            new_image= new_form.cleaned_data["imageURL"]
            category = new_form.cleaned_data["category"]
            create_listing = Listings(user=request.user, title=new_title, description=new_description, price=new_price, imageURL=new_image, category=category).save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {"form": new_form})
    else:
        return render(request, "auctions/create.html", {"form": CreateForm()})

def categories(request):
    categories = Listings.CATEGORY_CHOICES
    category_list = []
    for category in categories:
        category_list.append(category[1])
    return render(request, "auctions/categories.html", {"categories": category_list})

def category_list(request, category):
    active_category_listing = Listings.objects.filter(category=category[:2].upper()).filter(active=True)
    if not active_category_listing:
        return render(request, "auctions/category_list.html", {"message": "No active listings available."})
    else:
        return render(request, "auctions/category_list.html", {"listings": active_category_listing})

@login_required
def add_comment(request, listing_id):
    listing_details = Listings.objects.get(id=listing_id)
    comments = Comments.objects.filter(listing=listing_details)
    print(comments)
    # Add comment option
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.cleaned_data["content"]
            print(new_comment)
            add_comment = Comments(commenter=request.user, content=new_comment, listing=listing_details).save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id)))
        else:
            return render(request, "auctions/listing.html", {"comment_message": "Invalid Comment", "listing": listing_details, "comment_form": comment_form, "comments": comments, "bid_form": BidForm()})
    else:
        return render(request, "auctions/listing.html", {"listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm()})


@login_required
def listing(request, listing_id):
    listing_details = Listings.objects.get(id=listing_id)
    comments = Comments.objects.filter(listing=listing_details)
    bids = Bids.objects.filter(listing=listing_details)
    bids_count = bids.count()
    
    # Add watchlist function
    listing = Listings.objects.annotate(highest_bid=Max('bids__bid_price')).get(id=listing_id)
    watchlist = listing in request.user.active_user.all()

    # Add bid option
    if request.method == "POST":
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.cleaned_data["bid_price"]
            if bids:
                highest_bid = bids.order_by('bid_price').last().bid_price
                if new_bid <= highest_bid:
                    return render(request, "auctions/listing.html", {"bid_message": "Bid Price must be higher than initial listing price", "listing": listing_details, "comment_form": CommentForm, "comments": comments, "bid_form": BidForm(), "current_price": highest_bid, "bids_count": bids_count, "watchlist": watchlist})
                else:
                    add_bid = Bids(bid_price=new_bid, bidder=request.user, listing=listing_details).save()
                    highest_bid = bids.order_by('bid_price').last().bid_price
                    bids_count = bids.count()
                    return render(request, "auctions/listing.html", {"listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm(), "current_price": highest_bid, "bids_count": bids_count, "watchlist": watchlist})
            else:
                if new_bid <= listing_details.price:
                    return render(request, "auctions/listing.html", {"bid_message": "Bid Price must be higher than initial listing price", "listing": listing_details, "comment_form": CommentForm, "comments": comments, "bid_form": BidForm(), "current_price": listing_details.price, "bids_count": bids_count, "watchlist": watchlist})
                else:
                    add_bid = Bids(bid_price=new_bid, bidder=request.user, listing=listing_details).save()
                    highest_bid = bids.order_by('bid_price').last().bid_price
                    bids_count = bids.count()
                    return render(request, "auctions/listing.html", {"listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm(), "current_price": highest_bid, "bids_count": bids_count, "watchlist": watchlist})
        else:
            return render(request, "auctions/listing.html", {"bid_message": "Invalid Bid", "listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm(), "current_price": listing_details.price, "bids_count": bids_count, "watchlist": watchlist})
    else:
        if bids:
            highest_bid = bids.order_by('bid_price').last().bid_price
            return render(request, "auctions/listing.html", {"listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm(), "current_price": highest_bid, "bids_count": bids_count, "watchlist": watchlist})
        else:
            return render(request, "auctions/listing.html", {"listing": listing_details, "comment_form": CommentForm(), "comments": comments, "bid_form": BidForm(), "current_price": listing_details.price, "bids_count": bids_count, "watchlist": watchlist})

@login_required
def watchlist_action(request, listing_id):
    # Add watchlist function
    listing = Listings.objects.annotate(highest_bid=Max('bids__bid_price')).get(id=listing_id)

    watchlist = listing in request.user.active_user.all()
    if watchlist:
        request.user.active_user.remove(listing)
    else:
        request.user.active_user.add(listing)
    return HttpResponseRedirect(reverse("listing", args=(listing_id)))

@login_required
def watchlist(request):
    listings = request.user.active_user.annotate(highest_bid=Max('bids__bid_price'))
    return render(request, "auctions/watchlist.html", {"listings": listings})
    


