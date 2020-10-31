from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("searches", views.search, name="searches"),
    path("new_page", views.new_page, name="new_page"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/", views.random, name="random-page")
]

