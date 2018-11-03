from django.shortcuts import redirect


class ProtectedViewMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_active:
            return redirect('/users/login/?next=%s' % request.path)
        return super().dispatch(request, *args, **kwargs)


class SaveProfileMixin:
    def form_valid(self, form):
        form.instance.profile = self.request.user.profile_user
        return super().form_valid(form)
