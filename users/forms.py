from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        help_text='Обязательное поле. Не более 150 символов.'
    )
    email = forms.EmailField(
        label='Email',
        required=True
    )
    role = forms.ChoiceField(
        label='Роль',
        choices=User.ROLE_CHOICES
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
        return username