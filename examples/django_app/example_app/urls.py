from django.conf.urls import url
from django.contrib import admin
from example_app.views import ChatterBotAppView, ChatterBotApiView


urlpatterns = [
    url(r'^$', ChatterBotAppView.as_view(), name='main'),
    url(r'^admin/', admin.site.urls, name='admin'),
    url(r'^api/chatterbot/', ChatterBotApiView.as_view(), name='chatterbot'),
]
