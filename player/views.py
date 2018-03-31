import re
import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction, IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db.models import Max
from django.db.models import Min
from isro.settings import MEDIA_URL

import PIL

from .forms import LoginForm
from .models import Image


def play(request):
    if request.session.get('is_configured'):
        start_date_time = request.session['start_date_time']
        end_date_time = request.session['end_date_time']
        images = Image.objects.filter(date_time__gte=start_date_time, date_time__lte=end_date_time)
        image_list = []
        lat_start_ratio = int(float(request.session['lat_start_ratio']) * 100)
        lat_end_ratio = int(float(request.session['lat_end_ratio']) * 100)
        long_start_ratio = int(float(request.session['long_start_ratio']) * 100)
        long_end_ratio = int(float(request.session['long_end_ratio']) * 100)

        for image in images:
            try:
                if 'tmp' in image.image.name:
                    continue
                img = PIL.Image.open(image.image)
                width, height = img.size
                startX = long_start_ratio * width // 100;
                startY = lat_start_ratio * height // 100;
                endX = startX + (long_end_ratio - lat_start_ratio) * width // 100
                endY = startY + (lat_end_ratio - lat_start_ratio) * height // 100
                #print(startX, startY, endX, endY)
                x = img.crop((startY, startX, endY, endX))
                #print(x)
                #x.show() 
                name = 'uploads/tmp'+image.image.name.split('uploads/')[1]
                x.save(MEDIA_URL[1:] + name)
                image_list.append(MEDIA_URL[1:] + name)
            except Exception as e:
                print(e)
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


DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'

def date_time_range_is_valid(date_time1, date_time2):
    max_datetime = str(Image.objects.all().aggregate(Max('date_time'))['date_time__max'])[:-9]
    min_datetime = str(Image.objects.all().aggregate(Min('date_time'))['date_time__min'])[:-9]
    if max_datetime and min_datetime:
        return (time.strptime(date_time1, DATE_TIME_FORMAT) < time.strptime(date_time2, DATE_TIME_FORMAT)
            and time.strptime(min_datetime, DATE_TIME_FORMAT) <= time.strptime(date_time1, DATE_TIME_FORMAT)
            and time.strptime(date_time2, DATE_TIME_FORMAT) <= time.strptime(max_datetime, DATE_TIME_FORMAT))
    
    return False
    

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
            request.session['start_date'] = start_date
            request.session['start_time'] = start_time
            request.session['end_date'] = end_date
            request.session['end_time'] = end_time

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
def upload(request):
    imageRegex = re.compile(r'3DIMG_(\d{2})(\w{3})(\d{4})_(\d{2})(\d{2})_.+\.jpg')
    if request.method == 'POST':
        warning = None
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

                try:
                    with transaction.atomic():
                        Image.objects.create(image_type=image_type, date_time=date_time, image=image)
                except IntegrityError:
                    warning = 'Some images were duplicates, they were not uploaded'
        
        return render(request, 'player/play.html', {
            'warning': warning,
        })
    
    return render(request, 'player/upload.html', {})
