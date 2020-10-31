from django.shortcuts import render

from . import util

from builtins import any as b_any


from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect

from django.urls import reverse

from random import choice

from .forms import NewSearchForm, NewPageForm, EditPageForm

form = NewSearchForm()

def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries(), "form":form})

def title(request, title):
    if title in util.list_entries():
        return render(request, "encyclopedia/title.html", {"title": title, "content": util.get_entry(title), "form": form})
    else:
        return HttpResponseNotFound('<h3>Page was not found</h3>')


def search(request):
    if request.method == "GET":
        form = NewSearchForm(request.GET)
        if form.is_valid():
            search = form.cleaned_data["search"]
            search_result = [entry for entry in util.list_entries() if search in entry.casefold()]
            if util.get_entry(search):
                return render(request, "encyclopedia/title.html", {"title": search, "content": util.get_entry(search), "form": form})
            elif search_result:
                return render(request, "encyclopedia/searches.html", {"search_result": search_result, "form": form})
            else:
                return HttpResponseNotFound('<h3>No Result</h3>')
        else:
            return render(request, "encyclopedia/index.html")
    else:
        return render(request, "encyclopedia/index.html", {"form": form})


def new_page(request):
    if request.method == "POST":
        new_form = NewPageForm(request.POST)
        if new_form.is_valid():
            new_title = new_form.cleaned_data["title"]
            new_content = new_form.cleaned_data["content"]
            for entry in util.list_entries():
                if new_title.casefold() == entry.casefold():
                    return HttpResponseBadRequest('<h3>Entry Duplicated</h3>')
            util.save_entry(new_title, new_content)
            return render(request, "encyclopedia/title.html", {"title": new_title, "content": util.get_entry(new_title), "form": form})
        else:
            return render(request, "encyclopedia/new_page.html", {"new_form": new_form, "form": form})
    else:
        new_form = NewPageForm()
        return render(request, "encyclopedia/new_page.html", {"new_form": new_form, "form": form})



def edit(request, title):
    if request.method == "POST":
        edit_form = EditPageForm(request.POST)
        if edit_form.is_valid():
            updated_content = edit_form.cleaned_data["content"]
            util.save_entry(title, updated_content)
            return render(request, "encyclopedia/title.html", {"title": title, "content": util.get_entry(title), "form": form})
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": EditPageForm(initial={'content': content}), "form": form})


def random(request):
    if request.method == "GET":
        random_title = choice(util.list_entries())
        return render(request, "encyclopedia/title.html", {"title": random_title, "content": util.get_entry(random_title), "form": form})