from datetime import timezone
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from blog.models import Post


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "users/registration.html", {"form": form})


@login_required
def edit_profile(request, username):
    if request.user.username != username:
        return redirect("users:profile", username=username)
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("users:profile", username=username)
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=author).order_by("-pub_date")
    if request.user != author:
        now = timezone.now()
        posts = posts.filter(
            pub_date__lte=now, is_published=True, category__is_published=True
        )
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request, "user/profile.html",
        {"user_profile": author, "posts": page_obj}
    )
