from django.db import models
from .user import User
from .event import Event

class Signup(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='signups')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signups')

    def __str__(self):
        return f"<Signup id={self.id} event_id={self.event.id} user_id={self.user.id}>"
