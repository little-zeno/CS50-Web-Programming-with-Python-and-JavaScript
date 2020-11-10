from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:listing_id>", views.listing, name="listing"),
    path("add_comment/<str:listing_id>", views.add_comment, name="add_comment"),
    path("watchlist_action/<str:listing_id>", views.watchlist_action, name="watchlist_action"),
    path("categories", views.categories, name="categories"),
    path("category_list/<str:category>", views.category_list, name="category_list"),
    path("watchlist", views.watchlist, name="watchlist")
]