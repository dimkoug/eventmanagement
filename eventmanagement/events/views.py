from core.views import (
    CoreListView, CoreDetailView, CoreCreateView,
    CoreUpdateView, CoreDeleteView
)

from .forms import CategoryForm, LocationForm, EventForm
from .models import Category, Location, Event, EventMedia
from .mixins import ProtectedViewMixin, SaveProfileMixin


class EventList(ProtectedViewMixin, CoreListView):
    model = Event
    paginate_by = 100
    template = 'list'
    queryset = Event.objects.select_related('profile', 'location', 'category')

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
    queryset = Event.objects.select_related(
                    'profile', 'location', 'category'
                    ).prefetch_related('eventmedia')


class EventCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Event
    form_class = EventForm
    template = 'form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.profile = self.request.user.profile
        obj.save()
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                if f.name.endswith(".jpg"):
                    EventMedia.objects.create(event=obj, image=f)
        return super().form_valid(form)


class EventUpdate(ProtectedViewMixin, CoreUpdateView):
    model = Event
    form_class = EventForm
    template = 'form'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.profile = self.request.user.profile
        obj.save()
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                if f.name.endswith(".jpg"):
                    EventMedia.objects.create(event=obj, image=f)
        return super().form_valid(form)


class EventDelete(ProtectedViewMixin, CoreDeleteView):
    model = Event
    template = 'confirm_delete'


class LocationList(ProtectedViewMixin, CoreListView):
    model = Location
    paginate_by = 100
    template = 'list'
    queryset = Location.objects.select_related('profile')

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
    queryset = Location.objects.select_related('profile')


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


class CategoryList(ProtectedViewMixin, CoreListView):
    model = Category
    paginate_by = 100
    template = 'list'
    queryset = Category.objects.select_related('profile')

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        q = self.request.GET.get('q')
        if q and q != '':
            qs = qs.filter(name__icontains=q)
        return qs


class CategoryDetail(ProtectedViewMixin, CoreDetailView):
    model = Category
    template = 'detail'
    queryset = Category.objects.select_related('profile')


class CategoryCreate(ProtectedViewMixin, SaveProfileMixin, CoreCreateView):
    model = Category
    form_class = CategoryForm
    template = 'form'


class CategoryUpdate(ProtectedViewMixin, CoreUpdateView):
    model = Category
    form_class = CategoryForm
    template = 'form'


class CategoryDelete(ProtectedViewMixin, CoreDeleteView):
    model = Category
    template = 'confirm_delete'
