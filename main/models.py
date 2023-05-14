from django.db import models

# Create your models here.

class Account(models.Model): # 아이디 패스워드 모델
    email = models.CharField(max_length = 50, unique=True)
    password = models.CharField(max_length = 64, null=False)
    name = models.CharField(max_length = 10)
    gender = models.CharField(max_length = 6)
    genre = models.CharField(max_length = 10)
    registrationDate = models.CharField(max_length = 20)
    

class MusicList(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    title = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)
    albumImageURL = models.CharField(max_length=1000, default='')
    #artistImage = s

class UsersMusic(models.Model):
    pass

# 검색 기록 모델
class SearchHistory(models.Model):
    user_id = models.CharField(max_length=100)
    query = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_id}: {self.query}'
