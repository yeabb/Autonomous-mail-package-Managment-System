from django.db import models

# Create your models here.

class BeforeEmailVerification(models.Model):
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    email=models.EmailField()
    code=models.IntegerField()
