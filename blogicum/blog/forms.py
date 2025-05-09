from django import forms
from .models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text", "category", "location",
                  "image", "pub_date", "is_published"]
        widgets = {
            "pub_date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"rows": 3}),
        }
