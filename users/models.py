from django.db import models
from django.contrib.auth.models import AbstractUser
import random
from django.utils.timezone import now
from datetime import timedelta 

# Create your models here.

class User(AbstractUser):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('manager', 'Manager'),
        ('administrator', 'Administrator'),
    ]
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    confirmation_code = models.CharField(max_length=100, null=True, blank=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    def generate_confirmation_code(self):
        self.confirmation_code = 'some_generated_code'
        self.code_expires_at = now() + timedelta(hours=24)