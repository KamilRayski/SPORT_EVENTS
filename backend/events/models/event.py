from django.db import models
from django.utils import timezone
from events.models.user import User

class Event(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(default=10)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')

    def __str__(self):
        return f"<Event id={self.id} title={self.title} creator_id={self.creator.id}>"
