from django.urls import path
from . import views


urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("search", views.search, name="search"),
    path("new_loc_search", views.new_loc_search, name="new_loc_search"),
    path("category_explore", views.category_explore, name="category_explore"),
    path("explore", views.explore, name="explore"),
    path("restaurants/show/<int:id>", views.show_restaurant, name='show_restaurant'),
    path("restaurants/favorite", views.favorite, name="favorite"),

    path("friends/explore", views.explore_friends, name="explore_friends"),
    path("friends/add/<int:friend_id>", views.add_friend, name="add_friend"),
    path("friends/remove/<int:friend_id>", views.remove_friend, name="remove_friend"),
    path("friend/<int:friend_id>", views.friend, name="friend"),

    path("user/show/<int:id>", views.show_user, name="show_user"),
    path("user/edit", views.edit_profile, name="edit_profile"),
    path("user/change_password", views.change_password, name="change_password"),

    path("review/create/<int:id>", views.create_review, name='create_review'),
    path("review/update/<int:id>", views.update_review, name='update_review'),
    path("review/delete/<int:id>", views.delete_review, name='delete_review'),

    path("ajax/autocomplete", views.autocomplete_model, name='autocomplete_model'),
    path("ajax/new_loc_autocomplete", views.new_loc_autocomplete, name="new_loc_autocomplete"),
    path("ajax/state_change", views.state_change, name="state_change"),
    path("ajax/city_change", views.city_change, name="city_change"),
    path("test", views.test, name='test'),
    
    
]