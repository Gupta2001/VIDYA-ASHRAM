
import email
from email import message
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User
from .models import *


class Contact(models.Model):
    sno =models.AutoField(primary_key=True)
    name=models.CharField(max_length=40)
    email=models.CharField(max_length=40)
    phone=models.CharField(max_length=12)
    desc=models.TextField()
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100 )
    is_verified = models.BooleanField(default=False)
    Dues=models.CharField(max_length=100, default="0")
    created_at = models.DateTimeField(auto_now_add=True)
    Name=models.CharField(max_length=100 )
    fathers_Name=models.CharField(max_length=100 )
    Email_id=models.CharField(max_length=100)
    Classes=models.CharField(max_length=100)
    message=models.TextField(default="There is No messages from Vidya Ashram")


    def __str__(self):
        return self.user.username

class Blog(models.Model):
    sno =models.AutoField(primary_key = True) 
    title=models.CharField(max_length=50)
    content=models.TextField()
    short_content=models.CharField(max_length=255, default="Some String")
    slug=models.CharField(max_length=100)
    time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title