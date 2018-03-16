from django.shortcuts import render


def index(request):
    return render(request, 'player/base.html', {})


def config(request):
    return render(request, 'player/config.html', {})
