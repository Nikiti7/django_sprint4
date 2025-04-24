from django.urls import path
from . import views
from .views import CustomLoginView

app_name = "users"

urlpatterns = [
    path("registration/", views.registration, name="registration"),
    path("profile/<str:username>/", views.profile, name="profile"),
    path("profile/<str:username>/edit/",
         views.edit_profile,
         name="edit_profile"),
    path("login/", CustomLoginView.as_view(), name="login")
]
