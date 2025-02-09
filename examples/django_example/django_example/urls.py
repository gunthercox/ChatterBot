"""
URL configuration for django_example project.
"""
from django.contrib import admin
from django.urls import path
from django_example.views import ChatterBotAppView, ChatterBotApiView


urlpatterns = [
    path('', ChatterBotAppView.as_view(), name='main'),
    path('api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
    path('admin/', admin.site.urls, name='admin'),
]
