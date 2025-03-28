"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses.views import create_course, course_detail, course_list
from rest_framework.authtoken import views as auth_views_rest
from users.views import register_user

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('courses.urls')),
    path('api/', include('lessons.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('courses/create/', create_course, name='create_course'),
    path('courses/<int:pk>/', course_detail, name='course_detail'),
    path('courses/', course_list, name='course_list'),
    path('api/auth/register/', register_user, name='register'),
    path('api/auth/token/', auth_views_rest.obtain_auth_token, name='token'),
]