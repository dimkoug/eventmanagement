from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, AuthenticationForm as BaseAuthenticationForm

from .models import CustomUser

from profiles.models import Profile

from cms.forms import DynamicForm


class AuthenticationForm(DynamicForm, BaseAuthenticationForm):
    username = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')


class UserCreationForm(DynamicForm, forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    nickname = forms.CharField(label='username')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_nickname(self):
        # Check that the two password entries match
        nickname = self.cleaned_data.get("nickname")
        exists = Profile.objects.filter(nickname=nickname).exists()
        if exists:
            raise forms.ValidationError("Nickname exists")
        return nickname

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
