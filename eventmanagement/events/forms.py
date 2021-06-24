from django import forms
from .models import Location, Event

from core.forms import BootstrapForm


class LocationForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Location
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)


class EventForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'location', 'start_date', 'end_date')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_date(self):
        data = self.cleaned_data['start_date']
        exists = Event.objects.filter(start_date=data)
        if exists:
            raise forms.ValidationError("Event Exists")
        return data
