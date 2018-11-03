from django.shortcuts import render
from django.contrib import messages
from django.conf import settings
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.views import LoginView as BaseLoginView
from django.core.mail import EmailMessage
from django.urls import reverse
from django.http import HttpResponseRedirect

from profiles.models import Profile

from .forms import AuthenticationForm

from .models import CustomUser
from .forms import UserCreationForm
from .tokens import account_activation_token


class LoginView(BaseLoginView):
    form_class = AuthenticationForm


def register_view(request):
    form = UserCreationForm()
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile = Profile(
                            user=user, nickname=form.cleaned_data["nickname"])
            profile.save()
            current_site = get_current_site(request)
            message = render_to_string('users/active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            subject = 'Activate your Password Management account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()
            messages.add_message(request, messages.INFO, 'Please confirm your email address to complete the registration')
            return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
    context['form'] = form
    return render(request, "users/registration.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.is_confirmed = True
        user.save()
        profile = Profile.objects.get(user=user)
        profile.status = Profile.ACCOUNT_APPROVED
        profile.save()
        messages.add_message(request, messages.INFO, 'Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.add_message(request, messages.INFO, 'Activation link is invalid!')

    return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))


def delete_profile(request, id):
    user = CustomUser.objects.get(pk=id)
    context = {}
    context['user'] = user
    if request.method == 'POST':
        if request.user.pk == id:
            user.delete()
        return HttpResponseRedirect(reverse(settings.LOGIN_REDIRECT_URL))
    return render(request, "users/delete_profile.html", context)
