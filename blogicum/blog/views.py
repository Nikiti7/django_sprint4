from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, Comment
from django.core.paginator import Paginator

from django.contrib.auth.decorators import login_required
from .forms import PostForm, CommentForm
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden

User = get_user_model()


def index(request):
    """
    Главная страница:
    Выводятся пять последних публикаций, у которых:
      - дата публикации не позже текущего времени,
      - is_published=True,
      - у связанной категории is_published=True.
    """
    now = timezone.now()
    posts = Post.objects.filter(
        pub_date__lte=now, is_published=True, category__is_published=True
    ).order_by("-pub_date")
    paginator = Paginator(posts, 10)  # по 10 постов на страницу
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "blog/index.html", {"posts": page_obj})


def category_posts(request, category_slug):
    """
    Страница категории:
    Если у запрошенной категории is_published=False – возвращается 404.
    Иначе выводятся публикации, принадлежащие этой категории, у которых:
      - is_published=True,
      - дата публикации не позже текущего времени.
    """
    category = get_object_or_404(Category,
                                 slug=category_slug,
                                 is_published=True)
    posts = Post.objects.filter(
        category=category, pub_date__lte=timezone.now(), is_published=True
    ).order_by("-pub_date")
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "blog/category.html",
        {"category": category, "posts": page_obj}
    )


def post_detail(request, pk):
    """
    Страница отдельной публикации:
    Возвращается публикация по первичному ключу, если:
      - дата публикации не позже текущего времени,
      - is_published=True,
      - у связанной категории is_published=True.
    Иначе – 404.
    """
    post = get_object_or_404(
        Post.objects.select_related("category"),
        pk=pk,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now(),
    )
    form = CommentForm()
    comments = post.comments.all()
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "form": form, 'comments': comments}
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("users:profile", username=request.user.username)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})


@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)

    if request.user != post.author:
        return redirect("blog:post_detail", pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", post_id=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_form.html",
        {"form": form, "is_edit": True, "post": post}
    )


@login_required
def add_comment(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect("blog:post_detail", pk=pk)
    else:
        form = CommentForm()
    return render(request,
                  "blog/post_detail.html",
                  {"post": post, "form": form})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, pk=comment_id, author=request.user, post_id=post_id
    )
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("blog:post_detail", pk=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request,
                  "blog/edit_comment.html",
                  {"form": form, "comment": comment})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.user != post.author:
        return HttpResponseForbidden()

    if request.method == "POST":
        post.delete()
        return redirect("blog:index")

    return render(request, "blog/delete_post.html", {"post": post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment, pk=comment_id, author=request.user, post_id=post_id)
    if request.user != comment.author:
        return HttpResponseForbidden()

    if request.method == "POST":
        comment.delete()
        return redirect("blog:post_detail", pk=post_id)

    return render(request,
                  "blog/delete_comment.html",
                  {"comment": comment})
