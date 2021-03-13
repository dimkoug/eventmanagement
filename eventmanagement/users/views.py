from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.views.generic import FormView

from .tokens import account_activation_token
from .forms import (UserCreationForm,UserAuthenticationForm,
                    UserPasswordResetForm,UserSetPasswordForm)
from .models import User



class UserLoginView(auth_views.LoginView):
    template_name = 'users/login.html'
    form_class = UserAuthenticationForm


class UserLogoutView(auth_views.LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)


class UserPasswordResetView(auth_views.PasswordResetView):
    email_template_name = 'users/password_reset_email.html'
    form_class = UserPasswordResetForm
    subject_template_name = 'users/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'users/password_reset_form.html'


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
    title = 'Password reset complete'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'
    title = 'Password reset sent'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'users/password_reset_confirm.html'
    title = 'Enter new password'



class AccountActivationSent(TemplateView):
    template_name = 'users/account_activation_sent.html'



class SignupView(FormView):
    form_class = UserCreationForm
    template_name = 'users/signup.html'

    def form_valid(self,form):
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(self.request)
            user.refresh_from_db()  # load the profile instance created by the signal
            user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            subject = 'Activate Your MySite Account'
            message = render_to_string('users/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('account_activation_sent')
        return super().form_valid(form)



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('home')
    else:
        return render(request, 'users/account_activation_invalid.html')
