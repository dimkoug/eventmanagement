from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.template.loader import render_to_string
from django.db.models import Prefetch, Q
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from core.functions import is_ajax
from core.mixins import PaginationMixin, ModelMixin, SuccessUrlMixin,FormMixin,QueryListMixin, AjaxDeleteMixin


from .forms import CategoryForm, LocationForm, EventForm
from .models import Category, Location, Event, EventMedia
from .mixins import ProtectedViewMixin, SaveProfileMixin

class BaseListView(PaginationMixin,QueryListMixin,ModelMixin, LoginRequiredMixin, ListView):
    def dispatch(self, *args, **kwargs):
        self.ajax_list_partial = '{}/partials/{}_list_partial.html'.format(self.model._meta.app_label,self.model.__name__.lower())
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        if is_ajax(request):
            html_form = render_to_string(
                self.ajax_list_partial, context, request)
            return JsonResponse(html_form, safe=False)
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset



class EventList(BaseListView):
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


class EventDetail(LoginRequiredMixin, DetailView):
    model = Event
    template = 'detail'
    queryset = Event.objects.select_related(
                    'profile', 'location', 'category'
                    ).prefetch_related('eventmedia')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class EventCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Event
    form_class = EventForm

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                if f.name.endswith(".jpg"):
                    EventMedia.objects.create(event=form.instance, image=f)
        return super().form_valid(form)


class EventUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Event
    form_class = EventForm
    template = 'form'
    queryset = Event.objects.select_related(
                    'profile', 'location', 'category'
                    ).prefetch_related('eventmedia')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset

    def form_valid(self, form):
        files = self.request.FILES.getlist('media')
        if files:
            for f in files:
                if f.name.endswith(".jpg"):
                    EventMedia.objects.create(event=form.instance, image=f)
        return super().form_valid(form)


class EventDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Event
    ajax_partial = 'partials/ajax_delete_modal.html'

    queryset = Event.objects.select_related(
                    'profile', 'location', 'category'
                    ).prefetch_related('eventmedia')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class LocationList(BaseListView):
    model = Location
    paginate_by = 100
    template = 'list'
    queryset = Location.objects.select_related('profile')

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        return qs


class LocationDetail(LoginRequiredMixin, DetailView):
    model = Location
    template = 'detail'
    queryset = Location.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class LocationCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Location
    form_class = LocationForm
    template = 'form'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)


class LocationUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Location
    form_class = LocationForm
    template = 'form'

    queryset = Location.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class LocationDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Location
    ajax_partial = 'partials/ajax_delete_modal.html'

    queryset = Location.objects.select_related(
                    'profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class CategoryList(BaseListView):
    model = Category
    paginate_by = 100
    template = 'list'
    queryset = Category.objects.select_related('profile')

    def get_queryset(self):
        qs = super().get_queryset().filter(
            profile=self.request.user.profile)
        return qs


class CategoryDetail(LoginRequiredMixin, DetailView):
    model = Category
    template = 'detail'
    queryset = Category.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class CategoryCreate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template = 'form'

    def form_valid(self, form):
        form.instance.profile = self.request.user.profile
        form.save()
        return super().form_valid(form)


class CategoryUpdate(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,FormMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template = 'form'

    queryset = Category.objects.select_related('profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset


class CategoryDelete(ModelMixin, LoginRequiredMixin,SuccessUrlMixin,AjaxDeleteMixin,DeleteView):
    model = Category
    ajax_partial = 'partials/ajax_delete_modal.html'

    queryset = Category.objects.select_related(
                    'profile')

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(profile_id=self.request.user.profile.id)
        return queryset
