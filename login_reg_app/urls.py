from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("register", views.register, name='register'),
    path("login", views.login, name='login'),
    # path("dashboard", views.dashboard, name='dashboard'),
    path("logout", views.logout, name='logout'),
    path("ajax/validate-email", views.validate_email, name="ajax_validate_email"),
    path("ajax/validate-username", views.validate_username, name="ajax_validate_username"),
    ]

