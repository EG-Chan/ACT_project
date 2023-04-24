from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

def index(request):
    return render(request, "main/main.html")
# Create your views here.


def login(request): #로그인
    # GET
    if request.method == 'GET':
    
        return render(
            request,
            'main/main.html', 
        )
    # POST
    id = request.POST.get('id')
    pw = request.POST.get('pw')

    try:
        s = account.objects.get(pk=id, pw=pw)
    except:
        return redirect('login')

    request.session['id'] = s.id
    
    return redirect('main')