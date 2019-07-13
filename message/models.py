from django.db import models

# Create your models here.

class From_mail(models.Model):
    form_mail_add = models.CharField(max_length=30,unique=True)
    passwd = models.CharField(max_length=20)
    in_time = models.DateTimeField(auto_now_add=True)
class To_mail(models.Model):
    to_mail = models.CharField(max_length=30,unique=True)
    in_time = models.DateTimeField(auto_now_add=True)

class Target(models.Model):
    target = models.CharField(max_length=20)
    value = models.CharField(max_length=10)
    in_time = models.DateTimeField(auto_now_add=True)
