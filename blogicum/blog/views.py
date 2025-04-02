from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


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
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    ).order_by('-pub_date')[:5]
    return render(request, 'blog/index.html', {'posts': posts})


def category_posts(request, category_slug):
    """
    Страница категории:
    Если у запрошенной категории is_published=False – возвращается 404.
    Иначе выводятся публикации, принадлежащие этой категории, у которых:
      - is_published=True,
      - дата публикации не позже текущего времени.
    """
    # Получаем категорию по slug, проверяя, что она опубликована
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True)
    now = timezone.now()
    posts = Post.objects.filter(
        category=category,
        pub_date__lte=now,
        is_published=True
    ).order_by('-pub_date')
    return render(request, 'blog/category.html',
                  {'category': category, 'posts': posts})


def post_detail(request, post_id):
    """
    Страница отдельной публикации:
    Возвращается публикация по первичному ключу, если:
      - дата публикации не позже текущего времени,
      - is_published=True,
      - у связанной категории is_published=True.
    Иначе – 404.
    """
    now = timezone.now()
    post = get_object_or_404(
        Post,
        pk=post_id,
        pub_date__lte=now,
        is_published=True,
        category__is_published=True
    )
    return render(request, 'blog/detail.html', {'post': post})
