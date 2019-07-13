from django.db import models

# Create your models here.
class Monitor(models.Model):
    ip_add = models.GenericIPAddressField()
    # mem_total = models.CharField(max_length=20)
    mem_free = models.CharField(max_length=20,null= True)
    free_cpu_percent = models.CharField(max_length=20,null=True)
    use_time = models.CharField(max_length=20)
    min_1 = models.FloatField(null=True)
    min_5 = models.FloatField(null=True)
    min_15 = models.FloatField(null=True)
    in_time = models.DateTimeField(auto_now_add=True)

