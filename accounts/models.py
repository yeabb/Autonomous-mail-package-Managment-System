from django.db import models
from django.utils import timezone
# Create your models here.

class BeforeEmailVerification(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField()
    code=models.IntegerField()
    initiation_time=models.DateTimeField()
    expire_time=models.DateTimeField()
