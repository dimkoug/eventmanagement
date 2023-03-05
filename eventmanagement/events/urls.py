from django.urls import path

from core.patterns import get_patterns

from .views import EventList
from .functions import (
    get_sb_locations_data,
    get_sb_categories_data
)


app_name = 'events'
urlpatterns = get_patterns('events', 'views') +[
    path('', EventList.as_view(), name='event-list'),
    path('get_sb_locations_data/', get_sb_locations_data, name='sb-locations'),
    path('get_sb_categories_data/', get_sb_categories_data, name='sb-categories'),

]
