from django.db import models
from django.utils import timezone
# Create your models here.

class BeforeEmailVerification(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField()
    username=models.CharField(max_length=200)
    code=models.IntegerField()
    initiation_time=models.DateTimeField()
    expire_time=models.DateTimeField()

class Parcel(models.Model):
    email=models.EmailField()
    box_num=models.CharField(max_length=200)
    entrance_time=models.DateTimeField()
    access_code=models.IntegerField()

class BoxList(models.Model):
    box_num=models.IntegerField()
    available=models.BooleanField(default=True)
    associated_customer=models.EmailField(null=True)
    filledTime=models.DateTimeField(null=True)