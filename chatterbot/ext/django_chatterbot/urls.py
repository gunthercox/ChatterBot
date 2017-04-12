from django.conf.urls import url
from django.contrib import admin
from .views import ChatterBotView


urlpatterns = [
    url(
        r'^$',
        ChatterBotView.as_view(),
        name='chatterbot',
    ),
]
