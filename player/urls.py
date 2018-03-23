from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('config', views.config, name='config'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('play', views.play, name='play'),
    path('upload', views.upload, name='upload'),
]
