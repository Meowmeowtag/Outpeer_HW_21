from django.urls import path, include
from rest_framework.routers import DefaultRouter
from lessons.views import LessonViewSet

router = DefaultRouter()
router.register(r'lessons', LessonViewSet, basename='lesson')

urlpatterns = router.urls

urlpatterns = [
    path('', include(router.urls)),
] 