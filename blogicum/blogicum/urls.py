from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("pages/", include("pages.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("auth/", include("users.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


def csrf_failure(request, reason=""):
    return render(request, "pages/403csrf.html", status=403)


def custom_404(request, exception):
    return render(request, "pages/404.html", status=404)


def custom_500(request):
    return render(request, "pages/500.html", status=500)


handler403 = csrf_failure
handler404 = custom_404
handler500 = custom_500
