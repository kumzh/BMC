from django.db import models

# Create your models here.

class LoginUser(models.Model):
    username = models.CharField(max_length=20)
    userpasswd = models.CharField(max_length=30)
    in_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        '''返回模型的字符串表示'''
        return self.username