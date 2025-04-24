# pages/views.py
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, TemplateView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from .models import Page


def index(request):
    return render(request, 'pages/index.html')


class PageIndexView(TemplateView):
    template_name = 'pages/index.html'


class PageDetailView(DetailView):
    model = Page
    template_name = "pages/page_detail.html"
    context_object_name = "page"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class PageCreateView(CreateView):
    model = Page
    fields = ["title", "slug", "content"]
    template_name = "pages/page_form.html"
    success_url = reverse_lazy("pages:page_list")


class PageUpdateView(UpdateView):
    model = Page
    fields = ["title", "slug", "content"]
    template_name = "pages/page_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_success_url(self):
        return reverse_lazy("pages:page_detail",
                            kwargs={"slug": self.object.slug})
