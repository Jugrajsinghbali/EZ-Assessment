from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('ops', 'Ops'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)    
    email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

from django.db import models
from django.conf import settings

class FileUpload(models.Model):
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} by {self.uploaded_by.username}"


