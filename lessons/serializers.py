from rest_framework import serializers
from lessons.models import Lesson
from courses.serializers import CourseSerializer


class LessonSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_order(self, value):
        if value < 1:
            raise serializers.ValidationError("Порядковый номер не может быть меньше 1")
        return value

    def validate(self, data):
        course = self.context['request'].data.get('course')
        if course and not self.context['request'].user.is_staff:
            if not course.is_active:
                raise serializers.ValidationError({
                    "course": "Нельзя добавлять уроки в неактивный курс"
                })
        return data


class LessonListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка уроков"""
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ('id', 'title', 'course', 'order') 