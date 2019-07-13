from django.db import models

# Create your models here.
class Host(models.Model):
    system = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(unique=True)
    community = models.CharField(max_length=10)
    in_time = models.DateTimeField(auto_now_add=True)
#
class Host_info(models.Model):
    host_name = models.CharField(max_length=30)
    int_num = models.IntegerField()
    total_memo = models.CharField(max_length=20)
    int_info = models.CharField(max_length=70)
    host_ip = models.GenericIPAddressField(unique=True)
    cpu_info = models.CharField(max_length=70)