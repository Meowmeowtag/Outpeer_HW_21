from rest_framework import serializers
from .models import Course
from users.models import User
from datetime import datetime, date
from django.utils.dateparse import parse_date

class CourseSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    teacher = serializers.HiddenField(default=serializers.CurrentUserDefault())
    students = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = '__all__'
        extra_kwargs = {
            'price': {'required': True},
            'is_active': {'default': False},
            'start_date': {'required': True},
            'end_date': {'required': True}
        }

    def validate(self, data):
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_active = data.get('is_active', False)
        
        # Проверяем даты
        current_date = date.today()
        
        if start_date < current_date:
            raise serializers.ValidationError({
                "start_date": "Дата начала не может быть в прошлом"
            })
            
        if start_date > end_date:
            raise serializers.ValidationError({
                "end_date": "Дата окончания должна быть позже даты начала"
            })

        # Проверяем активацию курса
        if is_active and start_date < current_date:
            raise serializers.ValidationError({
                "is_active": "Нельзя активировать курс с прошедшей датой начала"
            })
        
        return data

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Цена должна быть больше нуля")
        return value

    def validate_start_date(self, value):
        if isinstance(value, str):
            value = parse_date(value)
        current_date = date.today()
        if value < current_date:
            raise serializers.ValidationError("Дата начала не может быть в прошлом")
        return value

    def validate_end_date(self, value):
        if isinstance(value, str):
            value = parse_date(value)
        return value

    def validate_max_students(self, value):
        if value <= 0:
            raise serializers.ValidationError("Максимальное количество студентов должно быть больше нуля")
        return value

    def validate_is_active(self, value):
        if not value:
            return value
            
        start_date = self.initial_data.get('start_date')
        end_date = self.initial_data.get('end_date')
        
        if isinstance(start_date, str):
            start_date = parse_date(start_date)
        if isinstance(end_date, str):
            end_date = parse_date(end_date)
            
        current_date = datetime.now().date()
        
        if start_date > end_date:
            raise serializers.ValidationError("Нельзя активировать курс с некорректными датами")
        
        if start_date < current_date:
            raise serializers.ValidationError("Нельзя активировать курс с прошедшей датой начала")
            
        return value

    def validate_teacher(self, value):
        request = self.context.get('request')
        if not request.user.is_staff:
            return request.user
        return value

    def validate_preview_image(self, value):
        if not value:
            raise serializers.ValidationError("Необходимо загрузить изображение для превью")
        return value

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Описание курса не может быть пустым")
        return value

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Название курса не может быть пустым")
        return value 