# events/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    def __str__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"

class Event(models.Model):
    title = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(default=10)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')

    def __str__(self):
        return f"<Event id={self.id} title={self.title} creator_id={self.creator.id}>"

class Signup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signups')

    def __str__(self):
        return f"<Signup id={self.id} event_id={self.event.id} user_id={self.user.id}>"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="favorited_by")

    class Meta:
        unique_together = (('user', 'event'),)


    def __str__(self):
        return f"<Favorite id={self.id} user_id={self.user.id} event_id={self.event.id}>"
