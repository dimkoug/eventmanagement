from django import forms
from .models import Category, Location, Event

from core.forms import BootstrapForm


class CategoryForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop("request")
    #     super().__init__(*args, **kwargs)


class LocationForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name',)

class EventForm(BootstrapForm, forms.ModelForm):
    media = forms.FileField(widget=forms.ClearableFileInput(
                            attrs={'multiple': True}), required=False,
                            help_text='only .jpg files accepted')

    class Meta:
        model = Event
        fields = ('name', 'category', 'location', 'description',
                  'start_date', 'end_date')
