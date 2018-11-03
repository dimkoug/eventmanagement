from django.urls import reverse_lazy


class SuccessUrlMixin:
    def get_success_url(self):
        model_name = self.model.__name__.lower()
        return reverse_lazy('{}-list'.format(model_name))
