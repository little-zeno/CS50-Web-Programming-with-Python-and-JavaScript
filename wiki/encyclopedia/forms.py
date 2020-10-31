
from django import forms

class NewSearchForm(forms.Form):
    search = forms.CharField(label="", required=True, widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(label="Page Title", widget=forms.TextInput(attrs={'placeholder': 'Enter Page Title'}))
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'rows': '2', 'cols': '50', 'style': 'height: 170px'}))

class EditPageForm(forms.Form):
    content = forms.CharField(label="Page Content", widget=forms.Textarea(attrs={'rows': '2', 'cols': '50', 'style': 'height: 170px'}))