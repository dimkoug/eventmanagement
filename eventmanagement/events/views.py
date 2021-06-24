from core.views import (
    CoreListView, CoreDetailView, CoreCreateView,
    CoreUpdateView, CoreDeleteView
)

from .forms import LocationForm, EventForm
from .models import Location, Event, EventMedia
from .mixins import ProtectedViewMixin, SaveProfileMixin


class EventList(ProtectedViewMixin, CoreListView):
    model = Event
    paginate_by = 100
    template = 'list'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class EventDetail(ProtectedViewMixin, CoreDetailView):
    model = Event
    template = 'detail'


class EventCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Event
    form_class = EventForm
    template = 'form'

    def form_valid(self, form):
        obj = form.save()
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                EventMedia.objects.create(event=obj, image=f)
        return super().form_valid(form)


class EventUpdate(ProtectedViewMixin, CoreUpdateView):
    model = Event
    form_class = EventForm
    template = 'form'

    def form_valid(self, form):
        obj = form.save()
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                EventMedia.objects.create(event=obj, image=f)
        return super().form_valid(form)


class EventDelete(ProtectedViewMixin, CoreDeleteView):
    model = Event
    template = 'confirm_delete'


class LocationList(ProtectedViewMixin, CoreListView):
    model = Location
    paginate_by = 100
    template = 'list'

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class LocationDetail(ProtectedViewMixin, CoreDetailView):
    model = Location
    template = 'detail'


class LocationCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Location
    form_class = LocationForm
    template = 'form'


class LocationUpdate(ProtectedViewMixin, CoreUpdateView):
    model = Location
    form_class = LocationForm
    template = 'form'


class LocationDelete(ProtectedViewMixin, CoreDeleteView):
    model = Location
    template = 'confirm_delete'
