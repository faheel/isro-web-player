import re

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm
from .models import Image


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

MONTH_NUM = {
    'JAN': '01',
    'FEB': '02',
    'MAR': '03',
    'APR': '04',
    'MAY': '05',
    'JUN': '06',
    'JUL': '07',
    'AUG': '08',
    'SEP': '09',
    'OCT': '10',
    'NOV': '11',
    'DEC': '12'
}


@login_required
def upload(request):
    imageRegex = re.compile(r'3DIMG_(\d{2})(\w{3})(\d{4})_(\d{2})(\d{2})_.+\.jpg')
    if request.method == 'POST':
        image_type = request.POST['image-type']
        for key in request.FILES:
            for image in request.FILES.getlist(key):
                matches = imageRegex.match(image.name)
                day = matches.group(1)
                month = MONTH_NUM[matches.group(2)]
                year = matches.group(3)
                hour = matches.group(4)
                minute = matches.group(5)

                date = year + '-' + month + '-' + day
                time = hour + ':' + minute
                Image.objects.create(image_type=image_type, date=date, time=time, image=image)
        return HttpResponseRedirect('/')
    
    return render(request, 'player/upload.html', {})
