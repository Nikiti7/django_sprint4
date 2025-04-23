# pages/views.py
from django.views.generic import DetailView, CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Page

class PageDetailView(DetailView):
    model = Page
    template_name = 'pages/page_detail.html'
    context_object_name = 'page'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class PageCreateView(CreateView):
    model = Page
    fields = ['title', 'slug', 'content']
    template_name = 'pages/page_form.html'
    success_url = reverse_lazy('pages:page_list')


class PageUpdateView(UpdateView):
    model = Page
    fields = ['title', 'slug', 'content']
    template_name = 'pages/page_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_success_url(self):
        return reverse_lazy('pages:page_detail', kwargs={'slug': self.object.slug})

