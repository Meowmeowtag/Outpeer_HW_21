from django.urls import path, include
from rest_framework.routers import DefaultRouter
from courses.views import register, confirm_email, user_list

router = DefaultRouter()

urlpatterns = [
    path('register/', register, name='register'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
    path('users/', user_list, name='user_list'),
    path('', include(router.urls)),
]