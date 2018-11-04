from django import forms
from .models import Event

from cms.forms import DynamicForm


class EventForm(DynamicForm, forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date')

    def clean_date(self):
        data = self.cleaned_data['date']
        exists = Event.objects.filter(date=data)
        if exists:
            raise forms.ValidationError("Event Exists")
        return data
