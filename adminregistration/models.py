from django.db import models
from django.contrib.auth.models import User



class registration(models.Model):
    user = models.OneToOneField('auth.User')
    phonenumber = models.CharField(max_length=10,default='')
