from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = (
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('manager', 'Менеджер'),
    )
    
    role = models.CharField(max_length=10, choices=ROLES, default='student')
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=100, null=True, blank=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    def generate_confirmation_code(self):
        self.confirmation_code = 'some_generated_code'
        self.code_expires_at = now() + timedelta(hours=24)