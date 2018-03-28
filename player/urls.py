from django.urls import path

from . import views

urlpatterns = [
    path('', views.play, name='play'),
    path('config', views.config, name='config'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('upload', views.upload, name='upload'),
]
