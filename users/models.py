from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta

class User(AbstractUser):
    MANAGER = 'manager'
    TEACHER = 'teacher'
    STUDENT = 'student'
    
    ROLE_CHOICES = [
        (MANAGER, 'Менеджер'),
        (TEACHER, 'Учитель'),
        (STUDENT, 'Студент'),
    ]
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
    )
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=100, null=True, blank=True)
    code_expires_at = models.DateTimeField(null=True, blank=True)

    def generate_confirmation_code(self):
        self.confirmation_code = 'some_generated_code'
        self.code_expires_at = timezone.now() + timedelta(hours=24)