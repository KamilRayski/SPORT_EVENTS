from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=120, blank=True, default="")

    def __str__(self):
        return f"<User id={self.id} username={self.username} email={self.email}>"
