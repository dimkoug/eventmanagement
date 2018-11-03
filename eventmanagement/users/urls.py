from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.conf import settings
from .views import register_view, activate, LoginView, delete_profile


urlpatterns = [
    # url(r'^$', HomeView.as_view(), name='home'),
    re_path(r'^register/$', register_view, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        activate, name='users_activate'),
    re_path('login/', LoginView.as_view(), {
        'template_name': "registration/login.html"},
        name='login'),
    re_path('logout/', auth_views.LogoutView.as_view(),
        {'next_page': settings.LOGIN_REDIRECT_URL}, name='logout'),

    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(),
        {'template_name': "registration/password_reset_form.html"},
        name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(),
        {'template_name': "registration/password_reset_done.html"},
        name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(),
        {'template_name': "registration/password_reset_confirm.html"},
        name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(),
        {'template_name': "registration/password_reset_complete.html"},
        name='password_reset_complete'),
    path('delete/profile/<int:id>/', delete_profile, name='delete-profile')
]
