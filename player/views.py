import re
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max
from django.db.models import Min

from .forms import LoginForm
from .models import Image


def play(request):
    if request.session.get('is_configured'):
        start_date_time = request.session['start_date_time']
        end_date_time = request.session['end_date_time']
        images = Image.objects.filter(date_time__gte=start_date_time, date_time__lte=end_date_time)
        image_list = []
        for image in images:
            image_list.append(image.image.url)
                    
        #print(image_list)
        return render(request, 'player/play.html', {
            'images': image_list,
        })

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


date_time_FORMAT = '%Y-%m-%d %H:%M'

def date_time_range_is_valid(date_time1, date_time2):
    ma=Image.objects.all().aggregate(Max('date_time')).value()
    mi=Image.objects.all().aggregate(Min('date_time')).value()
    return time.strptime(mi, date_time_FORMAT) <= time.strptime(date_time1, date_time_FORMAT) and time.strptime(ma, date_time_FORMAT) >= time.strptime(date_time1, date_time_FORMAT) and time.strptime(mi, date_time_FORMAT) <= time.strptime(date_time2, date_time_FORMAT) and time.strptime(ma, date_time_FORMAT) >= time.strptime(date_time2, date_time_FORMAT)
    return time.strptime(date_time1, date_time_FORMAT) < time.strptime(date_time2, date_time_FORMAT)

def config(request):
    is_invalid = False
    if request.method == 'POST':
        request.session['player_type'] = request.POST['player-type']

        start_date = request.POST['start-date']
        start_time = request.POST['start-time']
        end_date = request.POST['end-date']
        end_time = request.POST['end-time']
        
        # check if one of the region ranges are present
        if request.POST.get('lat-start-ratio'):
            request.session['lat_start_ratio'] = request.POST['lat-start-ratio']
            request.session['lat_end_ratio'] = request.POST['lat-end-ratio']
            request.session['long_start_ratio'] = request.POST['long-start-ratio']
            request.session['long_end_ratio'] = request.POST['long-end-ratio']
        
        start_date_time = start_date + ' ' + start_time
        end_date_time = end_date + ' ' + end_time
        # validate date range
        if date_time_range_is_valid(start_date_time, end_date_time):
            request.session['start_date_time'] = start_date_time
            request.session['end_date_time'] = end_date_time
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

                date_time = year + '-' + month + '-' + day + ' ' + hour + ':' + minute
                Image.objects.create(image_type=image_type, date_time=date_time, image=image)
        return HttpResponseRedirect('/')
    
    return render(request, 'player/upload.html', {})
