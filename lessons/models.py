from django.db import models
from courses.models import Course

class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    course = models.ForeignKey(
        Course, 
        on_delete=models.CASCADE, 
        related_name='lessons',
        verbose_name='Курс'
    )

    materials_url = models.URLField(
        blank=True, 
        null=True,
        verbose_name='Ссылка на материалы'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name='Порядковый номер'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['course', 'order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
