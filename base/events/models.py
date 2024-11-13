from django.contrib.auth.models import User
from django.db import models


class Event(models.Model):
    """
    This class represents an event in the application.

    Attributes:
    title (CharField): The title of the event.
    description (TextField): A detailed description of the event.
    location (CharField): The location where the event will take place.
    date (DateTimeField): The date and time of the event.
    organizer (ForeignKey): The user who is organizing the event.
    invited_users (ManyToManyField): The users who are invited to the event.
    time_created (DateTimeField): The date and time when the event was created.

    Methods:
    __str__(self): Returns a string representation of the event in the format: '{pk}_{title}_{date}'.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}_{self.title}_{self.date}'

