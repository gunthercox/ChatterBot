from django.conf.urls import url
from django.contrib import admin
from chatterbot.ext.django_chatterbot import views


urlpatterns = [
    url(
        r'^$',
        views.ChatterBotView.as_view(),
        name='chatterbot',
    ),
    url(
        r'^/train/$',
        views.ChatterBotTrainingView.as_view(),
        name='train',
    ),
]
