from django.db import models
from django.utils import timezone
from profiles.models import Profile
from core.models import Timestamped
# Create your models here.


class Category(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        default_related_name = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name}"


class Location(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        default_related_name = 'locations'
        verbose_name = 'location'
        verbose_name_plural = 'locations'

    def __str__(self):
        return f"{self.name}"


class Event(Timestamped):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE,
                                 null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(default=timezone.now)

    class Meta:
        default_related_name = 'events'
        verbose_name = 'event'
        verbose_name_plural = 'events'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.name}"


class EventMedia(Timestamped):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="events/media/")

    class Meta:
        default_related_name = 'eventmedia'
        verbose_name = 'event media'
        verbose_name_plural = 'event media'
        ordering = ('-created',)

    def __str__(self):
        return f"{self.image.name}"
