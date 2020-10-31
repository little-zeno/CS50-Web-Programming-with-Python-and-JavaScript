from django.shortcuts import render

from . import util

from builtins import any as b_any

from django import forms

from django.http import HttpResponseNotFound, HttpResponseBadRequest, HttpResponseRedirect

from django.urls import reverse

from random import choice


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})

def title(request, title):
    for entry in util.list_entries():
        if title in entry:
            return render(request, "encyclopedia/title.html", {"title": title, "content": util.get_entry(title)})
        else:
            return HttpResponseNotFound('<h3>Page was not found</h3>')


def search(request):
    if request.method == 'GET':
        search = request.GET['q']
        search_result = [entry for entry in util.list_entries() if search in entry.casefold()]
        if search:
            if util.get_entry(search):
                return render(request, "encyclopedia/title.html", {"title": util.get_entry(search)})
            elif search_result:
                return render(request, "encyclopedia/searches.html", {"search_result": search_result})
            else:
                return HttpResponseNotFound('<h3>No Result</h3>')
        else:
            return render(request, "encyclopedia/index.html")
    else:
        return render(request, "encyclopedia/index.html")


def new_page(request):
    if request.method == "POST":
        new_title = request.POST['title']
        new_content = request.POST['content']
        for entry in util.list_entries():
            if new_title == entry:
                return HttpResponseBadRequest('<h3>Entry Duplicated</h3>')
        util.save_entry(new_title, new_content)
        return render(request, "encyclopedia/title.html", {"title": new_title, "content": util.get_entry(new_title)})
    else:
        return render(request, "encyclopedia/new_page.html")


def edit(request, title):
    if request.method == "POST":
        updated_title = request.POST['title']
        updated_content = request.POST['content']
        if not updated_title:
            return HttpResponseBadRequest('<h3>Missing Title</h3>')
        elif not updated_content:
            return HttpResponseBadRequest('<h3>Missing Content</h3>')
        else:
            util.save_entry(updated_title, updated_content)
            return render(request, "encyclopedia/title.html", {"title": updated_title, "content": util.get_entry(updated_title)})
    else:
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", {"title": title, "content": content})

def random(request):
    if request.method == "GET":
        random_title = choice(util.list_entries())
        return render(request, "encyclopedia/title.html", {"title": random_title, "content": util.get_entry(random_title)})