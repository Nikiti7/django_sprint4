from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    description = models.TextField("Описание")
    slug = models.SlugField(
        "Идентификатор",
        unique=True,
        blank=False,
        help_text=(
            "Идентификатор страницы для URL; разрешены символы латиницы, "
            "цифры, дефис и подчёркивание."
        ),
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=False,
        help_text=("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "Категории"


class Location(models.Model):
    name = models.CharField("Название места", max_length=256)
    is_published = models.BooleanField(
        "Опубликовано",
        default=True,
        help_text=("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "местоположение"
        verbose_name_plural = "Местоположения"


class Post(models.Model):
    title = models.CharField("Заголовок", max_length=256)
    text = models.TextField("Текст")
    image = models.ImageField(
        upload_to="posts/", blank=True, null=True, verbose_name="Изображение"
    )
    pub_date = models.DateTimeField(
        "Дата и время публикации",
        help_text=(
            "Если установить дату и время в будущем — "
            "можно делать отложенные публикации."
        ),
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор публикации"
    )
    location = models.ForeignKey(
        "blog.Location",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Местоположение",
    )
    category = models.ForeignKey(
        "blog.Category",
        on_delete=models.CASCADE,
        null=True,
        verbose_name="Категория"
    )
    is_published = models.BooleanField(
        "Опубликовано",
        default=False,
        help_text=("Снимите галочку, чтобы скрыть публикацию."),
    )
    created_at = models.DateTimeField("Добавлено", auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "публикация"
        verbose_name_plural = "Публикации"
        ordering = ["-pub_date"]


class Comment(models.Model):
    post = models.ForeignKey("Post",
                             on_delete=models.CASCADE,
                             related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.author} к посту "{self.post}"'
