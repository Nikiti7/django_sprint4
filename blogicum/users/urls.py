from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/edit/",
         views.edit_profile,
         name="edit_profile"),
    path("auth/<str:username>/", views.profile, name="profile")
]
