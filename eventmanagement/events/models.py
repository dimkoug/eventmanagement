import datetime
from django.db import models

from profiles.models import Profile

# Create your models here.


class Timestamped(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Event(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        default_related_name = 'events'
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name
