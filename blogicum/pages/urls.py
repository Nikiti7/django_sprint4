from django.urls import path
from . import views
from .views import PageDetailView, PageCreateView, PageUpdateView

app_name = "pages"

urlpatterns = [
    path('', views.index, name='index'),
    path("<slug:slug>/", PageDetailView.as_view(), name="page_detail"),
    path("<slug:slug>/edit/", PageUpdateView.as_view(), name="page_edit"),
    path("create/", PageCreateView.as_view(), name="page_create"),
]
