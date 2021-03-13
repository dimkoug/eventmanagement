from django.shortcuts import render
from django.urls import reverse_lazy
from django.db.models import Q

from core.views import CoreListView, CoreDetailView, CoreCreateView, CoreUpdateView, CoreDeleteView


from .forms import EventForm
from .models import Event
from .mixins import ProtectedViewMixin, SaveProfileMixin


class EventList(ProtectedViewMixin, CoreListView):
    model = Event
    paginate_by = 100
    template='list'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class EventDetail(ProtectedViewMixin, CoreDetailView):
    model = Event
    template='detail'


class EventCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Event
    form_class = EventForm
    template='form'


class EventUpdate(ProtectedViewMixin, CoreUpdateView):
    model = Event
    form_class = EventForm
    template='form'


class EventDelete(ProtectedViewMixin, CoreDeleteView):
    model = Event
    template='confirm_delete'
