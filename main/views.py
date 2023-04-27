from django.shortcuts import render, redirect
from main.models import Account
from django.http import HttpResponseRedirect

def index(request):
    return render(request, "main/main.html")
# Create your views here.

def login(request): #로그인
    if request.method == 'GET':
        return render(request, "main/login.html")
    id = request.POST.get('id')
    pw = request.POST.get('pw')

    try:
        s = Account.objects.get(pk=id, pw=pw)
    except:
        return redirect('login')
    
    request.session['info_id'] = s.id
    return redirect('main')


def logout(request):
    return render(request, "main/logout.html")

def signup(request):
    return render(request, 'main/signup.html')