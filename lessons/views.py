from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Lesson
from .serializers import LessonSerializer, LessonListSerializer
from courses.models import Course
from courses.permissions import IsManagerOrReadOnly

# Create your views here.

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return LessonListSerializer
        return LessonSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        course_id = self.request.query_params.get('course_id', None)
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def perform_create(self, serializer):
        course_id = self.request.data.get('course')
        if not self.request.user.is_staff:
            raise permissions.PermissionDenied("Только менеджеры могут создавать уроки")
        serializer.save(course_id=course_id)

    @action(detail=False, methods=['get'])
    def course_lessons(self, request):
        """Получение уроков конкретного курса"""
        course_id = request.query_params.get('course_id')
        if not course_id:
            return Response(
                {"error": "Укажите параметр course_id"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        lessons = self.get_queryset().filter(course_id=course_id)
        serializer = self.get_serializer(lessons, many=True)
        return Response(serializer.data)
