from django.shortcuts import render


def index(request):
    return render(request, 'player/base.html', {})


def config(request):
    return render(request, 'player/config.html', {})


def play(request):
    return render(request, 'player/play.html', {})
