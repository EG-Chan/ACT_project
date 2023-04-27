from django.db import models

# Create your models here.

class Account(models.Model): # 아이디 패스워드 모델
    id = models.CharField(max_length = 20, primary_key=True)
    pw = models.CharField(max_length = 20, null=True)
    email = models.EmailField(max_length = 20)
    name = models.CharField(max_length = 20)
