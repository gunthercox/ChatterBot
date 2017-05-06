from django.conf.urls import url
from .views import ChatterBotView


urlpatterns = [
    url(
        r'^$',
        ChatterBotView.as_view(),
        name='chatterbot',
    ),
]
