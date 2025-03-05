from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register, confirm_email, user_list

urlpatterns = [
    path("register/", register, name="register"),
    path("confirm-email/", confirm_email, name="confirm_email"),
    path("users/", user_list, name="user_list"),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]