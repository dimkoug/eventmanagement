from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .mixins import SuccessUrlMixin


class BaseList(ListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.model,
            'title': 'List'
        })
        return context


class BaseDetail(DetailView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.get_object(),
            'title': 'Detail'
        })
        return context


class BaseCreate(SuccessUrlMixin, CreateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.model,
            'title': 'Create'
        })
        return context


class BaseUpdate(SuccessUrlMixin, UpdateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.get_object(),
            'title': 'Update'
        })
        return context


class BaseDelete(SuccessUrlMixin, DeleteView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'model': self.get_object(),
            'title': 'Delete'
        })
        return context
