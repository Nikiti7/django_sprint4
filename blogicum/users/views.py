from datetime import timezone
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

from blog.models import Post

User = get_user_model()


def registration(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # <-- автоматически логиним пользователя
            return redirect("users:profile", username=user.username)
    else:
        form = UserCreationForm()
    return render(request,
                  "registration/registration_form.html",
                  {"form": form})


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
    user_profile = get_object_or_404(User, username=username)
    posts = Post.objects.filter(
        author=user_profile, is_published=True, pub_date__lte=timezone.now())
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "users/profile.html", {
        "user_profile": user_profile,
        "posts": page_obj,
        "page_obj": page_obj
    })


class CustomLoginView(LoginView):
    def get_success_url(self):
        return reverse_lazy("users:profile",
                            kwargs={"username": self.request.user.username})
