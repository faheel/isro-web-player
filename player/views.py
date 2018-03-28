import re
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm
from .models import Image


def play(request):
    if request.session.get('is_configured'):
        # fetch images
        return render(request, 'player/play.html', {})

    return HttpResponseRedirect('config')


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


DATETIME_FORMAT = '%Y-%m-%d %H:%M'

def datetime_range_is_valid(datetime_tuple1, datetime_tuple2):
    datetime1 = datetime_tuple1[0] + ' ' + datetime_tuple1[1]
    datetime2 = datetime_tuple2[0] + ' ' + datetime_tuple2[1]
    return time.strptime(datetime1, DATETIME_FORMAT) < time.strptime(datetime2, DATETIME_FORMAT)

def config(request):
    is_invalid = False
    if request.method == 'POST':
        request.session['player_type'] = request.POST['player-type']

        start_date = request.POST['start-date']
        end_date = request.POST['end-date']
        start_time = request.POST['start-time']
        end_time = request.POST['end-time']
        
        # check if one of the region ranges are present
        if request.POST.get('lat-start-ratio'):
            request.session['lat_start_ratio'] = request.POST['lat-start-ratio']
            request.session['lat_end_ratio'] = request.POST['lat-end-ratio']
            request.session['long_start_ratio'] = request.POST['long-start-ratio']
            request.session['long_end_ratio'] = request.POST['long-end-ratio']
        
        # validate date range
        if datetime_range_is_valid((start_date, start_time), (end_date, end_time)):
            request.session['start_date'] = start_date
            request.session['end_date'] = end_date
            request.session['start_time'] = start_time
            request.session['end_time'] = end_time
            # everything is valid, player is now configured
            request.session['is_configured'] = True
            return HttpResponseRedirect('/')
        else:
            is_invalid = True
    
    return render(request, 'player/config.html', {
        'is_invalid': is_invalid,
    })


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
@transaction.atomic
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
