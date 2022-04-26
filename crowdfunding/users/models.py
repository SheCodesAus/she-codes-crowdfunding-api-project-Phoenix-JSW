from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    bio = models.TextField(null=True)
    applicant = models.CharField(max_length=200, blank=True, default="Adopt")
    is_staff = models.BooleanField()
            
    def __str__(self):
        return self.username