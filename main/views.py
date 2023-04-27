from django.shortcuts import render, redirect
from main.models import Account
from django.http import HttpResponseRedirect

def index(request):
    return render(request, "main/main.html")
# Create your views here.

def login(request): #로그인
    return render(request, "main/login.html")

def logout(request):
    return render(request, "main/logout.html")

def signup(request):
    return render(request, 'main/signup.html')