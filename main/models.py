from django.db import models

# Create your models here.

class Account(models.Model): # 아이디 패스워드 모델
    email = models.EmailField(max_length = 40)
    password = models.CharField(max_length = 20, null=False)
    name = models.CharField(max_length = 10)
    gender = models.CharField(max_length = 6)
    genre = models.CharField(max_length = 10)
    registrationDate = models.DateField(max_length = 20)
    

class MusicList(models.Model):
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    #albumImage = 
    #artistImage = s
