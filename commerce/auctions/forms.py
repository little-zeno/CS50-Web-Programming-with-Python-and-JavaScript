# forms.py

from django import forms
from .models import Listings, Comments, Bids
from django.core.exceptions import ValidationError

class CreateForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['title', 'price', 'description', 'category', 'imageURL']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content', 'commenter']

class BidForm(forms.ModelForm):
    class Meta:
        model = Bids
        fields = ['bid_price']
    

