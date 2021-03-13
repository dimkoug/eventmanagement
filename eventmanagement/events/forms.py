from django import forms
from .models import Event

from core.forms import BootstrapForm


class EventForm(BootstrapForm, forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Event.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Event Exists")
        return data
