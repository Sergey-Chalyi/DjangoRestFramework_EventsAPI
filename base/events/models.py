from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(max_length=1000, null=False, blank=False)
    location = models.CharField(max_length=255, null=False, blank=False)
    date = models.DateTimeField(null=False, blank=False)
    organizer = models.CharField(max_length=255, null=False, blank=False)

    time_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk}_{self.title}_{self.date}'