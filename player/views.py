from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm


def index(request):
    return render(request, 'player/base.html', {})


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(request.GET.get('next', '/'))
        else:
            is_invalid = True
    else:
        login_form = LoginForm()
        is_invalid = False
    
    return render(request, 'player/login.html', {
        'form': login_form,
        'is_invalid': is_invalid,
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def config(request):
    return render(request, 'player/config.html', {})


def play(request):
    return render(request, 'player/play.html', {})


@login_required
def upload(request):
    return render(request, 'player/upload.html', {})
