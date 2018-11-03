from django.urls import path

from .views import (
    EventList, EventDetail, EventCreate, EventUpdate,
    EventDelete
)


urlpatterns = [
    path('', EventList.as_view(), name='event-list'),
    path('<int:pk>/', EventDetail.as_view(),
         name='event-detail'),
    path('create/', EventCreate.as_view(),
         name='event-create'),
    path('<int:pk>/update/', EventUpdate.as_view(),
         name='event-update'),
    path('<int:pk>/delete', EventDelete.as_view(),
         name='event-delete'),


]
