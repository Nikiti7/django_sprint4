from django.shortcuts import render


def about(request):
    """Статическая страница "О нас" """
    return render(request, 'pages/about.html')


def rules(request):
    """Статическая страница "Правила" """
    return render(request, 'pages/rules.html')
