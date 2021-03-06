from django.conf import settings
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import JsonResponse
from django import template
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages


class DynamicTemplateMixin:
    '''
    Create template dynamically
    '''
    def get_template_names(self):
        model_name = self.model.__name__.lower()
        view_template = ""
        app = self.model._meta.app_label
        if not hasattr(self, 'template'):
            raise AttributeError(
                "Add template attribute to your {}  for example if list view"
                " then add template='list' appropriate values"
                " list,detail,form, confirm_delete".format(self.__class__.__name__)
            )
        view_template =  "{}/{}_{}.html".format(app,model_name, self.template)
        return [view_template]


class ModelMixin:
    '''
    Add  app and model to context
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        context['model_name'] = self.model.__name__.lower()
        context['app_name'] = self.model._meta.app_label
        return context


class UUidMixinQuery:
    def get_object(self, queryset=None):
        if queryset is None:
            queryset = super().get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is not None:
            queryset = queryset.filter(uuid=pk)
        obj = queryset.get()
        return obj


class SuccessUrlMixin:
    def get_success_url(self):
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        return reverse_lazy("{}:{}-list".format(app, model_name))


class FormMixin:
    def form_valid(self, form):
        obj = form.save()
        model_name = self.model.__name__.lower()
        app = self.model._meta.app_label
        if 'new' in self.request.POST:
            return redirect(reverse_lazy("{}:{}-create".format(app, model_name)))
        if 'continue' in self.request.POST:
            return redirect(reverse_lazy("{}:{}-update".format(app, model_name), kwargs={"pk":obj.pk}))
        if not self.request.is_ajax():
            messages.success(
                self.request, 'Your {} was proccesed successfully!'.format(
                    self.model.__name__))
        return super().form_valid(form)

    def form_invalid(self, form, **kwargs):
        data = dict()
        for field in form.errors:
            form[field].field.widget.attrs['class'] += ' is-invalid'
        context = self.get_context_data(form=form)
        if hasattr(self, 'ajax_partial'):
            data['html_form'] = render_to_string(
                self.ajax_partial, context, request=self.request)
        if self.request.is_ajax():
            return JsonResponse(data)
        else:
            messages.error(
                self.request, 'error ocured for {}'.format(
                    self.model.__name__))
            return self.render_to_response(self.get_context_data(form=form))


class ObjectMixin:
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)


class AjaxCreateMixin:
    def get(self, request, *args, **kwargs):
        self.object = None
        context = self.get_context_data()
        if request.is_ajax():
            html_form = render_to_string(
                self.ajax_partial, context, request)
            return JsonResponse({'html_form': html_form})
        else:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            obj = form.save()
            if obj:
                data['form_is_valid'] = True
                data['list'] = render_to_string(
                    self.ajax_list_partial, context, self.request)
            else:
                data['form_is_valid'] = False
                return super().form_invalid(form)
            data['html_form'] = render_to_string(
                self.ajax_partial, context, request=self.request)
            if self.request.is_ajax():
                return JsonResponse(data)
            else:
                return super().form_valid(form)
        else:
            return super().form_invalid(form)


class AjaxUpdateMixin(ObjectMixin):
    def form_valid(self, form):
        data = dict()
        context = self.get_context_data()
        if form.is_valid():
            obj = form.save()
            if obj:
                data['form_is_valid'] = True
                data['list'] = render_to_string(
                    self.ajax_list_partial, context, self.request)
            else:
                data['form_is_valid'] = False
            data['html_form'] = render_to_string(
                self.ajax_partial, context, request=self.request)
            if self.request.is_ajax():
                return JsonResponse(data)
            else:
                return super().form_valid(form)
        else:
            return super().form_invalid(form)


class AjaxDeleteMixin(ObjectMixin):
    def post(self, *args, **kwargs):
        if self.request.is_ajax():
            self.object = self.get_object()
            self.object.delete()
            data = dict()
            data['form_is_valid'] = True
            context = self.get_context_data()
            context['object_list'] = self.get_queryset()
            data['list'] = render_to_string(
                self.ajax_list_partial, context, self.request)
            return JsonResponse(data)
        else:
            return self.delete(*args, **kwargs)


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

class BaseViewMixin(LoginRequiredMixin, DynamicTemplateMixin,
                    ModelMixin):
    pass

class FormViewMixin(BaseViewMixin,SuccessUrlMixin,PassRequestToFormViewMixin, FormMixin):
    pass
