from django.contrib.auth.models import User
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    location = models.CharField(max_length=255)
    date = models.DateTimeField(null=True, blank=True)
    organizer = models.ForeignKey(User, related_name='organized_events', on_delete=models.CASCADE)
    invited_users = models.ManyToManyField(User, related_name='invited_events', blank=True)
    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}_{self.title}_{self.date}'

