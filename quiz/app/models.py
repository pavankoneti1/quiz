from django.db import models

# Create your models here.
class Subjects(models.Model):
    subject = models.CharField(max_length=20, primary_key= True, name='subject')
    def __str__(self):
        return f'{self.subject}'
class Questions(models.Model):
    sub = models.ForeignKey(Subjects, on_delete=models.CASCADE, name='sub', null=True)
    question = models.CharField(max_length=50,null=True, name='question')
    option1 = models.CharField(max_length=10, null=False, blank=False, name='option1')
    option2 = models.CharField(max_length=10, null=False, blank=False, name='option2')
    option3 = models.CharField(max_length=10, null=True, blank=True, name='option3')
    option4 = models.CharField(max_length=10, null=True, blank=True, name='option4')
    public = models.BooleanField(default=True, name='public')
    key = models.IntegerField(null=True, blank=True, name='key')

