from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model

User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    preview_image = models.ImageField(upload_to='course_previews/', verbose_name='Превью', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_courses')
    students = models.ManyToManyField(User, related_name='enrolled_courses')
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    max_students = models.PositiveIntegerField(default=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now().date() + timedelta(days=30)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title 