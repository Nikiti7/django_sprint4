from django.shortcuts import render

def about(request):
    """Статическая страница "О нас" """
    return render(request, 'about.html')

def rules(request):
    """Статическая страница "Правила" """
    return render(request, 'rules.html')


