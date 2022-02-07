from turtle import ondrag
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass


class Jogging(models.Model):
    date = models.DateTimeField()
    distance = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)