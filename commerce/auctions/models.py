from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    active_user = models.ManyToManyField("Listings", blank=True, related_name="active_user")

class Listings(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    FASHION = 'FA'
    TOYS = 'TO'
    ELECTRONICS = 'EL'
    HOME = 'HO'
    CATEGORY_CHOICES = [(FASHION, 'Fashion'), (TOYS, 'Toys'), (ELECTRONICS, 'Electronics'), (HOME, 'Home'),]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    imageURL = models.URLField(max_length=20000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="buyer")

    def __str__(self):
        return self.title

class Bids(models.Model):
    bid_price = models.DecimalField(decimal_places=2, max_digits=10, null=True)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids", null=True)
    bid_date = models.DateTimeField(auto_now_add=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", null=True)
    
    def __str__(self):
        return f"{self.bidder} bids {self.listing} for ${self.bid_price} at {self.bid_date}"

class Comments(models.Model):
    content = models.CharField(max_length=300)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comment", null=True)
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter", null=True)
    comment_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.commenter} commented {self.content} about {self.listing} on {self.comment_date}"