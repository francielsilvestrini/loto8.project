from django.shortcuts import render


def homepage(request):
    return render(request, 'homepage.html')


def sobre(request):
    return render(request, 'sobre.html')