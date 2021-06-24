from django.urls import path

from core.patterns import get_patterns

from .views import EventList

app_name = 'events'
urlpatterns = get_patterns('events', 'views') +[
    path('', EventList.as_view(), name='event-list'),
]
