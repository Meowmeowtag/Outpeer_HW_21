from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.crypto import get_random_string
import logging
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Course
from .serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from users.models import User
from lessons.permissions import IsManagerUser
from .forms import RegistrationForm, CourseForm
from courses.permissions import IsManagerOrReadOnly

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, 'Регистрация успешна! Теперь вы можете войти.')
                return redirect('login')
            except Exception as e:
                user.delete()
                messages.error(request, f'Ошибка при регистрации: {str(e)}')
        else:
            logger.error(f"Form errors: {form.errors}")
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

def confirm_email(request):
    if request.method == "POST":
        email = request.POST.get("email")
        code = request.POST.get("code")
        
        logger.info(f"Attempting to confirm email for {email} with code {code}")
        
        try:
            user = User.objects.get(
                email=email,
                confirmation_code=code,
                is_active=False
            )
            
            user.is_active = True
            user.confirmation_code = None
            user.save()
            
            logger.info(f"Successfully confirmed email for user {email}")
            messages.success(request, 'Email успешно подтвержден! Теперь вы можете войти.')
            return redirect('login')
            
        except User.DoesNotExist:
            logger.error(f"Invalid confirmation attempt for {email}")
            messages.error(request, 'Неверный код подтверждения или email')
            return render(request, "users/confirm_email.html", {
                "error": "Неверный код подтверждения или email",
                "email": email
            })
            
    return render(request, "users/confirm_email.html")

def user_list(request):
    users = User.objects.all()
    paginator = Paginator(users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'users/user_list.html', {'page_obj': page_obj})

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.IsAuthenticated, IsManagerOrReadOnly]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsManagerUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['post'])
    def add_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            if course.students.count() >= course.max_students:
                return Response({'error': 'Course is full'}, status=400)
            course.students.add(student)
            return Response({'status': 'student enrolled'})
        except User.DoesNotExist:
            return Response({'error': 'student not found'}, status=404)

    @action(detail=True, methods=['post'])
    def remove_student(self, request, pk=None):
        course = self.get_object()
        student_id = request.data.get('student_id')
        
        try:
            student = User.objects.get(id=student_id, role='student')
            course.students.remove(student)
            return Response({'status': 'student removed'})
        except User.DoesNotExist:
            return Response({'error': 'student not found'}, status=404)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.author = request.user
            course.save()
            messages.success(request, 'Курс успешно создан!')
            return redirect('course_detail', pk=course.pk)
    else:
        form = CourseForm()
    return render(request, 'courses/course_form.html', {'form': form})

def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'courses/course_detail.html', {'course': course})

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})