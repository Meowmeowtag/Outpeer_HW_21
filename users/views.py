from django.shortcuts import render
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.utils.timezone import now
from .forms import RegistrationForm
from .models import User
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.crypto import get_random_string
import logging
from django.contrib import messages

logger = logging.getLogger(__name__)


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        logger.info("Processing registration form")
        
        if form.is_valid():
            logger.info("Form is valid")
            try:
                user = form.save(commit=False)
                user.is_active = False
                user.confirmation_code = get_random_string(length=6)
                user.save()
                logger.info(f"User created: {user.email}")

                logger.info(f"Attempting to send email to {user.email}")
                send_mail(
                    'Подтверждение регистрации',
                    f'Ваш код подтверждения: {user.confirmation_code}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                logger.info(f"Email sent successfully to {user.email}")
                return redirect('confirm_email')
            except Exception as e:
                logger.error(f"Error during registration: {str(e)}")
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