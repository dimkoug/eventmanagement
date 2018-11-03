from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from cms.views import BaseList, BaseDetail, BaseCreate, BaseUpdate, BaseDelete


from .forms import EventForm
from .models import Event
from .mixins import ProtectedViewMixin, SaveProfileMixin


class EventList(ProtectedViewMixin, BaseList):
    model = Event
    paginate_by = 100

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile_user)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class EventDetail(ProtectedViewMixin, BaseDetail):
    model = Event


class EventCreate(ProtectedViewMixin, SaveProfileMixin, BaseCreate):
    model = Event
    form_class = EventForm


class EventUpdate(ProtectedViewMixin, BaseUpdate):
    model = Event
    form_class = EventForm


class EventDelete(ProtectedViewMixin, BaseDelete):
    model = Event
    success_url = reverse_lazy('event-list')
