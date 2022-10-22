from django.db import models

# Create your models here.
class Users(models.Model):
    first=models.CharField(max_length=20,name='first')
    last=models.CharField(max_length=20,name='last', null=True)
    email = models.EmailField(name='email')
    password = models.CharField(max_length=20, name='passeword')

class LoginForm(models.Model):
    username = models.CharField(max_length=20, name='username')
    password = models.CharField(max_length=20, name='passeword')
