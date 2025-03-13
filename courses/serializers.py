from rest_framework import serializers
from .models import Course
from users.models import User

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'teacher', 'students', 
                 'start_date', 'end_date', 'max_students', 'is_active',
                 'created_at', 'updated_at'] 