from django.db import models

# Create your models here.

class Members(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    adress = models.CharField(max_length = 255, null = True, blank = True)
    phone = models.IntegerField(null=True)
    joined_date = models.DateTimeField(null=True)

    