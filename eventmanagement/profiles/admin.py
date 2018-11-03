from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from .models import Profile



class ProfileAdmin(admin.ModelAdmin):
    model = Profile

admin.site.register(Profile, ProfileAdmin)
