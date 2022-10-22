from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import LoginForm
class AuthForm(AuthenticationForm):
    class Meta:
        model = LoginForm()
        # fields = ('username', 'password')
        fields = '__all__'