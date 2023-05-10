from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

#
from datetime import datetime
import hashlib

#모델
from main.models import Account

#스포티파이
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# mp3 저장
import wget

# pandas, numpy
import pandas as pd
import numpy as np

# 모델 불러오기
import joblib
import requests
import os

# service2, 4 음원 분석 라이브러리
import scipy.io.wavfile
from scipy.fftpack import dct
import librosa
import tensorflow as tf
from pydub import AudioSegment

def main(request):
    return render(request, "main/main.html")
# Create your views here.

def login(request): #로그인
    # 일반적인 접속인 경우
    if request.method == "GET":
        context = {"state" : 0}
        return render(request, "main/login.html", context=context)
    
    #로그인 버튼을 누른경우
    elif request.method == "POST":
        context = None
        email = request.POST.get("email")
        password = request.POST.get("password")

        #비밀번호 암호화
        hlib = hashlib.sha256()
        hlib.update(password.encode("UTF-8"))
        password = hlib.hexdigest()

        try:
            #DB에서 email이 같은 레코드와 비교
            user = Account.objects.get(email=email)
            if email == user.email and password == user.password:
                request.session["email"] = email
                request.session["userName"] = user.name
                context = {
                    "sessionID" : request.session.session_key,
                    "userName" : request.session["userName"],
                }
                return render(request, "main/main.html", context=context)
            else:
                context = {
                    "state" : 1,
                    "email" : email,
                }
                return render(request, "main/login.html", context=context)
        
        #없는 이메일을 입력한 경우
        except:
            context = {
                "state" : 2,
                "email" : email,
            }
            return render(request, "main/login.html", context=context)
        # except:

        #     context = {"state" : 3}
        #     print("실행2")
        #     return render(request, "main/login.html", context=context)
            


def logout(request):
    #세션정보 모두 삭제
    request.session.flush()

    return redirect("/")

def signup(request):
    # 일반적인 접속인 경우
    # context에 따라 다른 웹페이지가 보이게함
    if request.method == "GET": 
        context = {"state" : 0}
        return render(request, "main/signup.html", context=context)
    
    # 회원가입버튼을 누른경우
    elif request.method == "POST":
        context = None
        try:
            email = request.POST.get("email")
            password = request.POST.get("password")
            name = request.POST.get("name")
            gender = request.POST.get("gender")
            genre = request.POST.get("genre")

            #비밀번호 암호화
            hlib = hashlib.sha256()
            hlib.update(password.encode("UTF-8"))
            hlib.hexdigest()

            #DB에 저장
            user = Account()
            user.email = email
            user.password = hlib.hexdigest()
            user.name = name
            user.gender = gender
            user.genre = genre
            user.registrationDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user.save()

            context = {"state" : 1}
        except:
            context = {"state" : 2}
        finally:
            return render(request, "main/signup.html", context=context)
        
def userInfo(request):
    context = {
        "email": request.session["email"]
    }
    return render(request, "main/userInfo.html", context=context)

def search(request):
    if request.method == "POST":
        search = request.POST.get("search")

        # client_id=''
        # client_secret=''
        # client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        # sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        #artist = sp.search(q=f'{search}', type='track')
        artist = {'tracks':{'href':'https://api.spotify.com/v1/search?query=chandelier&type=track&offset=0&limit=10','items':[{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/6FdNvoO5sF4EKwCX9je1MH'},'href':'https://api.spotify.com/v1/albums/6FdNvoO5sF4EKwCX9je1MH','id':'6FdNvoO5sF4EKwCX9je1MH','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273b55ed804149fffbb5e35ff34','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02b55ed804149fffbb5e35ff34','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851b55ed804149fffbb5e35ff34','width':64}],'name':'1000 Forms Of Fear (Deluxe Version)','release_date':'2015-05-04','release_date_precision':'day','total_tracks':20,'type':'album','uri':'spotify:album:6FdNvoO5sF4EKwCX9je1MH'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AR','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':216120,'explicit':False,'external_ids':{'isrc':'USRC11400498'},'external_urls':{'spotify':'https://open.spotify.com/track/2s1sdSqGcKxpPr5lCl7jAV'},'href':'https://api.spotify.com/v1/tracks/2s1sdSqGcKxpPr5lCl7jAV','id':'2s1sdSqGcKxpPr5lCl7jAV','is_local':False,'name':'Chandelier','popularity':72,'preview_url':'https://p.scdn.co/mp3-preview/fa13db3d66f6daf051e9a3996090f7740532b9e8?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':1,'type':'track','uri':'spotify:track:2s1sdSqGcKxpPr5lCl7jAV'},{'album':{'album_group':'single','album_type':'single','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/0oouuXi8tdasgUgk520Jy6'},'href':'https://api.spotify.com/v1/artists/0oouuXi8tdasgUgk520Jy6','id':'0oouuXi8tdasgUgk520Jy6','name':'Will Paquin','type':'artist','uri':'spotify:artist:0oouuXi8tdasgUgk520Jy6'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/1VC4P7rm1o3aYlYVYFkpGF'},'href':'https://api.spotify.com/v1/albums/1VC4P7rm1o3aYlYVYFkpGF','id':'1VC4P7rm1o3aYlYVYFkpGF','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b27309cb96e3e43c6ac1c240888d','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e0209cb96e3e43c6ac1c240888d','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d0000485109cb96e3e43c6ac1c240888d','width':64}],'name':'Chandelier','release_date':'2020-09-25','release_date_precision':'day','total_tracks':1,'type':'album','uri':'spotify:album:1VC4P7rm1o3aYlYVYFkpGF'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/0oouuXi8tdasgUgk520Jy6'},'href':'https://api.spotify.com/v1/artists/0oouuXi8tdasgUgk520Jy6','id':'0oouuXi8tdasgUgk520Jy6','name':'Will Paquin','type':'artist','uri':'spotify:artist:0oouuXi8tdasgUgk520Jy6'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':127464,'explicit':False,'external_ids':{'isrc':'QM24S2009107'},'external_urls':{'spotify':'https://open.spotify.com/track/1cwqP7Tyxu5z8XDYoPkNte'},'href':'https://api.spotify.com/v1/tracks/1cwqP7Tyxu5z8XDYoPkNte','id':'1cwqP7Tyxu5z8XDYoPkNte','is_local':False,'name':'Chandelier','popularity':74,'preview_url':'https://p.scdn.co/mp3-preview/64e41bd2d79267b8eb43dcdc15acd10cb37af33a?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':1,'type':'track','uri':'spotify:track:1cwqP7Tyxu5z8XDYoPkNte'},{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/6FdNvoO5sF4EKwCX9je1MH'},'href':'https://api.spotify.com/v1/albums/6FdNvoO5sF4EKwCX9je1MH','id':'6FdNvoO5sF4EKwCX9je1MH','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273b55ed804149fffbb5e35ff34','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02b55ed804149fffbb5e35ff34','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851b55ed804149fffbb5e35ff34','width':64}],'name':'1000 Forms Of Fear (Deluxe Version)','release_date':'2015-05-04','release_date_precision':'day','total_tracks':20,'type':'album','uri':'spotify:album:6FdNvoO5sF4EKwCX9je1MH'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AR','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':241693,'explicit':False,'external_ids':{'isrc':'USRC11402032'},'external_urls':{'spotify':'https://open.spotify.com/track/0Ha4WnjeGxmsnzTnlEvjvZ'},'href':'https://api.spotify.com/v1/tracks/0Ha4WnjeGxmsnzTnlEvjvZ','id':'0Ha4WnjeGxmsnzTnlEvjvZ','is_local':False,'name':'Chandelier - Piano Version','popularity':59,'preview_url':'https://p.scdn.co/mp3-preview/373937a7d1a5b7430357a5a8800e75938d7c5cbf?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':13,'type':'track','uri':'spotify:track:0Ha4WnjeGxmsnzTnlEvjvZ'},{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/6MERXsiRbur2oJZFgYRDKz'},'href':'https://api.spotify.com/v1/artists/6MERXsiRbur2oJZFgYRDKz','id':'6MERXsiRbur2oJZFgYRDKz','name':'Vitamin String Quartet','type':'artist','uri':'spotify:artist:6MERXsiRbur2oJZFgYRDKz'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/3kXPzEHhPKArQtzlQmPR9N'},'href':'https://api.spotify.com/v1/albums/3kXPzEHhPKArQtzlQmPR9N','id':'3kXPzEHhPKArQtzlQmPR9N','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b2732d0ab6a2d85dfaed6e239a8b','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e022d0ab6a2d85dfaed6e239a8b','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d000048512d0ab6a2d85dfaed6e239a8b','width':64}],'name':'VSQ Performs the Hits of 2014, Vol. 2','release_date':'2014-08-19','release_date_precision':'day','total_tracks':8,'type':'album','uri':'spotify:album:3kXPzEHhPKArQtzlQmPR9N'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/6MERXsiRbur2oJZFgYRDKz'},'href':'https://api.spotify.com/v1/artists/6MERXsiRbur2oJZFgYRDKz','id':'6MERXsiRbur2oJZFgYRDKz','name':'Vitamin String Quartet','type':'artist','uri':'spotify:artist:6MERXsiRbur2oJZFgYRDKz'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':215000,'explicit':False,'external_ids':{'isrc':'USEWC1489121'},'external_urls':{'spotify':'https://open.spotify.com/track/5A51C7Ank2IRW0TmhYkeoK'},'href':'https://api.spotify.com/v1/tracks/5A51C7Ank2IRW0TmhYkeoK','id':'5A51C7Ank2IRW0TmhYkeoK','is_local':False,'name':'Chandelier','popularity':51,'preview_url':'https://p.scdn.co/mp3-preview/54d4cb83b893cec7773f622dae291bda91dca66b?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':5,'type':'track','uri':'spotify:track:5A51C7Ank2IRW0TmhYkeoK'},{'album':{'album_group':'single','album_type':'single','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','KE','KG','KH','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','OM','PA','PE','PH','PK','PL','PS','PT','PY','QA','RO','RS','RW','SA','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TR','TT','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/2fBKreCrztEPXW5bUIgBTf'},'href':'https://api.spotify.com/v1/albums/2fBKreCrztEPXW5bUIgBTf','id':'2fBKreCrztEPXW5bUIgBTf','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273858d8767593fd2db82a0def8','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02858d8767593fd2db82a0def8','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851858d8767593fd2db82a0def8','width':64}],'name':'Spotify Sessions','release_date':'2016-04-13','release_date_precision':'day','total_tracks':6,'type':'album','uri':'spotify:album:2fBKreCrztEPXW5bUIgBTf'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/5WUlDfRSoLAfcVSX1WnrxN'},'href':'https://api.spotify.com/v1/artists/5WUlDfRSoLAfcVSX1WnrxN','id':'5WUlDfRSoLAfcVSX1WnrxN','name':'Sia','type':'artist','uri':'spotify:artist:5WUlDfRSoLAfcVSX1WnrxN'}],'available_markets':['AR','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','GM','GE','GD','GW','GY','HT','JM','LS','LR','MW','MV','ML','FM','NA','NE','SM','ST','SN','SC','SL','KN','LC','VC','SR','TL','TT','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':237333,'explicit':False,'external_ids':{'isrc':'USRC11600687'},'external_urls':{'spotify':'https://open.spotify.com/track/2CZX6RHW9EYFhhTANVsF5A'},'href':'https://api.spotify.com/v1/tracks/2CZX6RHW9EYFhhTANVsF5A','id':'2CZX6RHW9EYFhhTANVsF5A','is_local':False,'name':'Chandelier - Live from The Village','popularity':54,'preview_url':'https://p.scdn.co/mp3-preview/a4f5622438a497bbf69ea1cf36a1d6fb0fc9ce5d?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':5,'type':'track','uri':'spotify:track:2CZX6RHW9EYFhhTANVsF5A'},{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/4tYSBptyGeVyZsk8JC4JHZ'},'href':'https://api.spotify.com/v1/artists/4tYSBptyGeVyZsk8JC4JHZ','id':'4tYSBptyGeVyZsk8JC4JHZ','name':'Shoreline Mafia','type':'artist','uri':'spotify:artist:4tYSBptyGeVyZsk8JC4JHZ'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/6lolOKwewTA3hoBA6FDTI0'},'href':'https://api.spotify.com/v1/albums/6lolOKwewTA3hoBA6FDTI0','id':'6lolOKwewTA3hoBA6FDTI0','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b2736bbce4b34887f5b056a5cb5f','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e026bbce4b34887f5b056a5cb5f','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d000048516bbce4b34887f5b056a5cb5f','width':64}],'name':'Party Pack. Vol 2','release_date':'2019-09-04','release_date_precision':'day','total_tracks':9,'type':'album','uri':'spotify:album:6lolOKwewTA3hoBA6FDTI0'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/4tYSBptyGeVyZsk8JC4JHZ'},'href':'https://api.spotify.com/v1/artists/4tYSBptyGeVyZsk8JC4JHZ','id':'4tYSBptyGeVyZsk8JC4JHZ','name':'Shoreline Mafia','type':'artist','uri':'spotify:artist:4tYSBptyGeVyZsk8JC4JHZ'},{'external_urls':{'spotify':'https://open.spotify.com/artist/3ppQEG71r7jVpI8RudzycF'},'href':'https://api.spotify.com/v1/artists/3ppQEG71r7jVpI8RudzycF','id':'3ppQEG71r7jVpI8RudzycF','name':'OHGEESY','type':'artist','uri':'spotify:artist:3ppQEG71r7jVpI8RudzycF'},{'external_urls':{'spotify':'https://open.spotify.com/artist/63GIj2yhFvX1Bzphb9JgVb'},'href':'https://api.spotify.com/v1/artists/63GIj2yhFvX1Bzphb9JgVb','id':'63GIj2yhFvX1Bzphb9JgVb','name':'Fenix Flexin','type':'artist','uri':'spotify:artist:63GIj2yhFvX1Bzphb9JgVb'},{'external_urls':{'spotify':'https://open.spotify.com/artist/6X8WdFjrNhXATMDSs26aCc'},'href':'https://api.spotify.com/v1/artists/6X8WdFjrNhXATMDSs26aCc','id':'6X8WdFjrNhXATMDSs26aCc','name':'Curren$y','type':'artist','uri':'spotify:artist:6X8WdFjrNhXATMDSs26aCc'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':212333,'explicit':True,'external_ids':{'isrc':'USAT21904823'},'external_urls':{'spotify':'https://open.spotify.com/track/0doPjH3V2qKDUKjfpW3k92'},'href':'https://api.spotify.com/v1/tracks/0doPjH3V2qKDUKjfpW3k92','id':'0doPjH3V2qKDUKjfpW3k92','is_local':False,'name':'Chandelier (feat. Curren$y)','popularity':51,'preview_url':'https://p.scdn.co/mp3-preview/0462be1d4ae17ab293f924a96efc53b62b003ec4?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':5,'type':'track','uri':'spotify:track:0doPjH3V2qKDUKjfpW3k92'},{'album':{'album_group':'single','album_type':'single','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/7IErGg6ZCfFyJJoKGUUBpv'},'href':'https://api.spotify.com/v1/artists/7IErGg6ZCfFyJJoKGUUBpv','id':'7IErGg6ZCfFyJJoKGUUBpv','name':'accelerate','type':'artist','uri':'spotify:artist:7IErGg6ZCfFyJJoKGUUBpv'},{'external_urls':{'spotify':'https://open.spotify.com/artist/2uSVRVjYZ0PlJPdFHnBETu'},'href':'https://api.spotify.com/v1/artists/2uSVRVjYZ0PlJPdFHnBETu','id':'2uSVRVjYZ0PlJPdFHnBETu','name':'creamy','type':'artist','uri':'spotify:artist:2uSVRVjYZ0PlJPdFHnBETu'},{'external_urls':{'spotify':'https://open.spotify.com/artist/2MDj296KJIfgWDNBtHzeFi'},'href':'https://api.spotify.com/v1/artists/2MDj296KJIfgWDNBtHzeFi','id':'2MDj296KJIfgWDNBtHzeFi','name':'11:11 Music Group','type':'artist','uri':'spotify:artist:2MDj296KJIfgWDNBtHzeFi'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/3wPxUXHLwYYHmOUSbPh7ru'},'href':'https://api.spotify.com/v1/albums/3wPxUXHLwYYHmOUSbPh7ru','id':'3wPxUXHLwYYHmOUSbPh7ru','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273860e9dabc25799309fd5db9a','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02860e9dabc25799309fd5db9a','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851860e9dabc25799309fd5db9a','width':64}],'name':'chandelier (sped up)','release_date':'2022-10-11','release_date_precision':'day','total_tracks':1,'type':'album','uri':'spotify:album:3wPxUXHLwYYHmOUSbPh7ru'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/7IErGg6ZCfFyJJoKGUUBpv'},'href':'https://api.spotify.com/v1/artists/7IErGg6ZCfFyJJoKGUUBpv','id':'7IErGg6ZCfFyJJoKGUUBpv','name':'accelerate','type':'artist','uri':'spotify:artist:7IErGg6ZCfFyJJoKGUUBpv'},{'external_urls':{'spotify':'https://open.spotify.com/artist/2uSVRVjYZ0PlJPdFHnBETu'},'href':'https://api.spotify.com/v1/artists/2uSVRVjYZ0PlJPdFHnBETu','id':'2uSVRVjYZ0PlJPdFHnBETu','name':'creamy','type':'artist','uri':'spotify:artist:2uSVRVjYZ0PlJPdFHnBETu'},{'external_urls':{'spotify':'https://open.spotify.com/artist/2MDj296KJIfgWDNBtHzeFi'},'href':'https://api.spotify.com/v1/artists/2MDj296KJIfgWDNBtHzeFi','id':'2MDj296KJIfgWDNBtHzeFi','name':'11:11 Music Group','type':'artist','uri':'spotify:artist:2MDj296KJIfgWDNBtHzeFi'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':108160,'explicit':False,'external_ids':{'isrc':'GX8KD2202762'},'external_urls':{'spotify':'https://open.spotify.com/track/5qJ8dIfppTNpFjGrq0gNvF'},'href':'https://api.spotify.com/v1/tracks/5qJ8dIfppTNpFjGrq0gNvF','id':'5qJ8dIfppTNpFjGrq0gNvF','is_local':False,'name':'chandelier (sped up)','popularity':39,'preview_url':'https://p.scdn.co/mp3-preview/0e78805fc5c644912c00c2848adeb2a750eca602?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':1,'type':'track','uri':'spotify:track:5qJ8dIfppTNpFjGrq0gNvF'},{'album':{'album_group':'single','album_type':'single','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/0oouuXi8tdasgUgk520Jy6'},'href':'https://api.spotify.com/v1/artists/0oouuXi8tdasgUgk520Jy6','id':'0oouuXi8tdasgUgk520Jy6','name':'Will Paquin','type':'artist','uri':'spotify:artist:0oouuXi8tdasgUgk520Jy6'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/2YbtxC0EEfKtYNURsYhzaA'},'href':'https://api.spotify.com/v1/albums/2YbtxC0EEfKtYNURsYhzaA','id':'2YbtxC0EEfKtYNURsYhzaA','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273471c775be003a96aabe3c4e1','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02471c775be003a96aabe3c4e1','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851471c775be003a96aabe3c4e1','width':64}],'name':'Chandelier (Instrumental Version)','release_date':'2020-09-27','release_date_precision':'day','total_tracks':1,'type':'album','uri':'spotify:album:2YbtxC0EEfKtYNURsYhzaA'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/0oouuXi8tdasgUgk520Jy6'},'href':'https://api.spotify.com/v1/artists/0oouuXi8tdasgUgk520Jy6','id':'0oouuXi8tdasgUgk520Jy6','name':'Will Paquin','type':'artist','uri':'spotify:artist:0oouuXi8tdasgUgk520Jy6'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':128000,'explicit':False,'external_ids':{'isrc':'QM24S2009206'},'external_urls':{'spotify':'https://open.spotify.com/track/7wzKnw2xHUe5FLrW5d8Dt8'},'href':'https://api.spotify.com/v1/tracks/7wzKnw2xHUe5FLrW5d8Dt8','id':'7wzKnw2xHUe5FLrW5d8Dt8','is_local':False,'name':'Chandelier (Instrumental Version)','popularity':46,'preview_url':'https://p.scdn.co/mp3-preview/33dc60587c0549bf1fe6d3ec0a07bd0f0badc897?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':1,'type':'track','uri':'spotify:track:7wzKnw2xHUe5FLrW5d8Dt8'},{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/3YfvowVavHTzXLKmKaYM1c'},'href':'https://api.spotify.com/v1/artists/3YfvowVavHTzXLKmKaYM1c','id':'3YfvowVavHTzXLKmKaYM1c','name':'Beloved Melodies','type':'artist','uri':'spotify:artist:3YfvowVavHTzXLKmKaYM1c'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/2o84UpZFhVixlpEzKemhhx'},'href':'https://api.spotify.com/v1/albums/2o84UpZFhVixlpEzKemhhx','id':'2o84UpZFhVixlpEzKemhhx','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b273bfe0526011ee547912411147','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e02bfe0526011ee547912411147','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d00004851bfe0526011ee547912411147','width':64}],'name':'Beloved Melodies','release_date':'2020-04-17','release_date_precision':'day','total_tracks':12,'type':'album','uri':'spotify:album:2o84UpZFhVixlpEzKemhhx'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/3YfvowVavHTzXLKmKaYM1c'},'href':'https://api.spotify.com/v1/artists/3YfvowVavHTzXLKmKaYM1c','id':'3YfvowVavHTzXLKmKaYM1c','name':'Beloved Melodies','type':'artist','uri':'spotify:artist:3YfvowVavHTzXLKmKaYM1c'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':128500,'explicit':False,'external_ids':{'isrc':'SEBGA2000269'},'external_urls':{'spotify':'https://open.spotify.com/track/4Pp5lXQYGe1M6gpMs2fpg0'},'href':'https://api.spotify.com/v1/tracks/4Pp5lXQYGe1M6gpMs2fpg0','id':'4Pp5lXQYGe1M6gpMs2fpg0','is_local':False,'name':'Chandelier','popularity':54,'preview_url':'https://p.scdn.co/mp3-preview/0e4d9c684ad11d3f7d59db3b809a75da570e8f3e?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':11,'type':'track','uri':'spotify:track:4Pp5lXQYGe1M6gpMs2fpg0'},{'album':{'album_group':'album','album_type':'album','artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/6TV0LZ3BaEun0OQEh96elP'},'href':'https://api.spotify.com/v1/artists/6TV0LZ3BaEun0OQEh96elP','id':'6TV0LZ3BaEun0OQEh96elP','name':'Jordan Smith','type':'artist','uri':'spotify:artist:6TV0LZ3BaEun0OQEh96elP'}],'available_markets':['AD','AE','AG','AL','AM','AO','AR','AT','AU','AZ','BA','BB','BD','BE','BF','BG','BH','BI','BJ','BN','BO','BR','BS','BT','BW','BY','BZ','CA','CD','CG','CH','CI','CL','CM','CO','CR','CV','CW','CY','CZ','DE','DJ','DK','DM','DO','DZ','EC','EE','EG','ES','ET','FI','FJ','FM','FR','GA','GB','GD','GE','GH','GM','GN','GQ','GR','GT','GW','GY','HK','HN','HR','HT','HU','ID','IE','IL','IN','IQ','IS','IT','JM','JO','JP','KE','KG','KH','KI','KM','KN','KR','KW','KZ','LA','LB','LC','LI','LK','LR','LS','LT','LU','LV','LY','MA','MC','MD','ME','MG','MH','MK','ML','MN','MO','MR','MT','MU','MV','MW','MX','MY','MZ','NA','NE','NG','NI','NL','NO','NP','NR','NZ','OM','PA','PE','PG','PH','PK','PL','PS','PT','PW','PY','QA','RO','RS','RW','SA','SB','SC','SE','SG','SI','SK','SL','SM','SN','SR','ST','SV','SZ','TD','TG','TH','TJ','TL','TN','TO','TR','TT','TV','TW','TZ','UA','UG','US','UY','UZ','VC','VE','VN','VU','WS','XK','ZA','ZM','ZW'],'external_urls':{'spotify':'https://open.spotify.com/album/144abioSp1P3RFW1HujUsX'},'href':'https://api.spotify.com/v1/albums/144abioSp1P3RFW1HujUsX','id':'144abioSp1P3RFW1HujUsX','images':[{'height':640,'url':'https://i.scdn.co/image/ab67616d0000b2733d9a8c19e38f38383e37323a','width':640},{'height':300,'url':'https://i.scdn.co/image/ab67616d00001e023d9a8c19e38f38383e37323a','width':300},{'height':64,'url':'https://i.scdn.co/image/ab67616d000048513d9a8c19e38f38383e37323a','width':64}],'name':'The Complete Season 9 Collection (The Voice Performance)','release_date':'2015-12-16','release_date_precision':'day','total_tracks':11,'type':'album','uri':'spotify:album:144abioSp1P3RFW1HujUsX'},'artists':[{'external_urls':{'spotify':'https://open.spotify.com/artist/6TV0LZ3BaEun0OQEh96elP'},'href':'https://api.spotify.com/v1/artists/6TV0LZ3BaEun0OQEh96elP','id':'6TV0LZ3BaEun0OQEh96elP','name':'Jordan Smith','type':'artist','uri':'spotify:artist:6TV0LZ3BaEun0OQEh96elP'}],'available_markets':['AR','AU','AT','BE','BO','BR','BG','CA','CL','CO','CR','CY','CZ','DK','DO','DE','EC','EE','SV','FI','FR','GR','GT','HN','HK','HU','IS','IE','IT','LV','LT','LU','MY','MT','MX','NL','NZ','NI','NO','PA','PY','PE','PH','PL','PT','SG','SK','ES','SE','CH','TW','TR','UY','US','GB','AD','LI','MC','ID','JP','TH','VN','RO','IL','ZA','SA','AE','BH','QA','OM','KW','EG','MA','DZ','TN','LB','JO','PS','IN','BY','KZ','MD','UA','AL','BA','HR','ME','MK','RS','SI','KR','BD','PK','LK','GH','KE','NG','TZ','UG','AG','AM','BS','BB','BZ','BT','BW','BF','CV','CW','DM','FJ','GM','GE','GD','GW','GY','HT','JM','KI','LS','LR','MW','MV','ML','MH','FM','NA','NR','NE','PW','PG','WS','SM','ST','SN','SC','SL','SB','KN','LC','VC','SR','TL','TO','TT','TV','VU','AZ','BN','BI','KH','CM','TD','KM','GQ','SZ','GA','GN','KG','LA','MO','MR','MN','NP','RW','TG','UZ','ZW','BJ','MG','MU','MZ','AO','CI','DJ','ZM','CD','CG','IQ','LY','TJ','VE','ET','XK'],'disc_number':1,'duration_ms':200200,'explicit':False,'external_ids':{'isrc':'USUM71514364'},'external_urls':{'spotify':'https://open.spotify.com/track/77TWynyVX80ekKTmtQyhpJ'},'href':'https://api.spotify.com/v1/tracks/77TWynyVX80ekKTmtQyhpJ','id':'77TWynyVX80ekKTmtQyhpJ','is_local':False,'name':'Chandelier - The Voice Performance','popularity':44,'preview_url':'https://p.scdn.co/mp3-preview/9ec53ad4b81c55299131de458cd67a1ccff98bdd?cid=baa750d0d8984735b51fa1c31b643d0b','track_number':1,'type':'track','uri':'spotify:track:77TWynyVX80ekKTmtQyhpJ'}],'limit':10,'next':'https://api.spotify.com/v1/search?query=chandelier&type=track&offset=10&limit=10','offset':0,'previous':None,'total':1000}}

        return render(request, "main/search.html", {"spotipyDatas":artist})
    return render(request, "main/search.html")

# step 2 genres 축양을 위한 리스트화
def genreList(genres):
    genre_list = []
    # 장르별 조건 주기
    for i in genres:
        if i == '':
            genre_list.append('ect')
        elif (i.find('indie') != -1) or (i.find('singer-songwriter') != -1):
            genre_list.append('indie')
        elif (i.find('rock') != -1) or (i.find('alt') != -1) or (i.find('drum and bass') != -1) or (i.find('metal') != -1) \
            or (i.find('old school') != -1) or (i.find('band') != -1) or (i.find('punk') != -1) or (i.find('mellow gold') != -1) \
            or (i.find('grunge') != -1):
            genre_list.append('rock')
        elif (i.find('uplift') != -1) or (i.find('swing') != -1) or (i.find('jazz') != -1) or (i.find('black') != -1) \
            or (i.find('motown') != -1):
            genre_list.append('black')
        elif (i.find('futur') != -1) or (i.find('city') != -1) or (i.find('mordern') != -1):
            genre_list.append('future')
        elif (i.find('country') != -1) or (i.find('folk') != -1) or (i.find('redneck') != -1) or (i.find('torch song') != -1):
            genre_list.append('country')
        elif (i.find('house') != -1) or (i.find('ton') != -1) or (i.find('tropical') != -1) or (i.find('complextro') != -1)  :
            genre_list.append('edm')
        elif (i.find('edm') != -1) or (i.find('drop') != -1) or (i.find('dup') != -1) or (i.find('big room') != -1) or (i.find('electro') != -1)\
            or (i.find('gymcore') != -1) or (i.find('nightcore') != -1) or (i.find('azontobeats') != -1):
            genre_list.append('edm')
        elif (i.find('funk') != -1) :
            genre_list.append('funk')
        elif (i.find('techno') != -1) or (i.find('uk') != -1) or (i.find('disco') != -1) :
            genre_list.append('edm')
        elif (i.find('soul') != -1) or (i.find('r&b') != -1) or (i.find('vibe') != -1) or (i.find('urbano') != -1) or (i.find('quiet storm') != -1)\
            or (i.find('urban contemporary') != -1):
            genre_list.append('rnb')
        elif (i.find('rap') != -1) or (i.find('trap') != -1) or (i.find('hip hop') != -1) or (i.find('drill') != -1) or (i.find('boom bap') != -1) \
            or (i.find('plugg') != -1):
            genre_list.append('rap')
        elif (i.find('wave') != -1) or (i.find('syns') != -1) or (i.find('trance') != -1) :
            genre_list.append('syns')
        elif i.find('new') != -1:
            genre_list.append('newage')
        elif (i.find('dance') != -1) or (i.find('girl group') != -1):
            genre_list.append('dance')
        elif i.find('pop') != -1:
            genre_list.append('pop')
        elif (i.find('baiano') != -1) or (i.find('mexicana') != -1) or (i.find('western') != -1) or (i.find('sierreno') != -1) \
            or (i.find('vallenato') != -1) or (i.find('corrido') != -1) or (i.find('yodeling') != -1):
            genre_list.append('world')
        elif (i.find('easy') != -1) or (i.find('lounge') != -1):
            genre_list.append('relax')
        elif (i.find('show') != -1) or (i.find('movie') != -1) or (i.find('hollywood') != -1) or (i.find('sped up') != -1) or (i.find('ost') != -1):
            genre_list.append('media')
        else :
            genre_list.append('ect')

    # 중복장르 제거
    return list(set(genre_list))

# 장르 최소화
def changeGenres(x):
    if 'ect' in x:
        return 'ect'
    elif 'indie' in x:
        return 'indie'
    elif 'world' in x:
        return 'world'
    elif 'rock' in x:
        return 'rock'
    elif 'funk' in x:
        return 'funk'
    elif 'retro' in x:
        return 'retro'
    elif 'dance' in x:
        return 'dance'
    elif 'media' in x:
        return 'media'
    elif 'relax' in x:
        return 'relax'
    elif 'edm' in x:
        return 'edm'
    elif 'house' in x:
        return 'edm'
    elif 'syns' in x:
        return 'edm'
    elif 'black' in x:
        return 'black'
    elif 'rnb' in x:
        return 'black'
    elif 'country' in x:
        return 'country'
    elif 'newage' in x:
        return 'newage'
    elif 'rap' in x:
        return 'rap'
    else : 
        # 여기에도 없는 태그일 경우 그냥 전부 pop으로 보기
        return 'pop'

# tempo 변경
def changeTempo(x):
    if x[0] == 'rap':
        if x[1] >= 120 :
            return x[1] / 2
        else :
            return x[1]
    else :
        return x[1]
def serviceCheck(service):
    if 1 in service:
        return '빌보드 가능성 있음'
    else :
        return '빌보드 가능성 거의 없음'
def findIndie(artist_name):
    urls = 'https://en.wikipedia.org/wiki/'
    response = requests.get(urls + artist_name)
    if ('indie' in response.text) or ('on TikTok' in response.text) or ('Underground' in response.text) or ('minor hit' in response.text) or \
        ('meme' in response.text) or ('Challenge' in response.text) or ('DJ' in response.text) or ('GYM' in response.text) :
        return 1
    else :
        return 0

def checkIndie(artist_name, indie):
    not_indie_list = [
    'Taylor Swift','Lil Uzi Vert',  'The Weeknd', 'Juice WRLD', 'Pop Smoke', 'Dua Lipa',
    'Drake', 'Future', 'Lil Baby', 'Gunna', 'Polo G', 'Bad Bunny', 'DaBaby', 'Billie Eilish',
    'Ariana Grande', 'Harry Styles', 'BLACKPINK', 'SZA', 'Maroon 5', 'Lizzo', 'Mariah Carey', 
    'YoungBoy Never Broke Again', 'Cardi B', 'Halsey', 'Soulja Boy', 'Travis Scott', 'Justin Bieber',
    'Britney Spears', 'Lil Keed', 'Lady Gaga', 'Avril Lavigne', 'Olivia Rodrigo', 'J. Cole','Daddy Yankee',
    'Lily Allen', 'Thundercat', 'Anne Marie','BTS', 'Macklemore & Ryan Lewis', 'Ella Mai', 'Imagine Dragons',
    '24KGoldn', 'Labrinth', 'Christina Perri', 'Nicki Minaj', 'Chris Brown', 'Selena Gomez', 'Meghan Trainor', 
    'Kesha', 'Katy Perry', 'Kelly Clarkson', 'Black Eyed Peas', 'Michael Jackson', 'KAROL G', 'Beyonce',
    'Charlie Puth', 'Ed Sheeran', 'Roddy Ricch', 'Alicia Keys','Sia'
    ]

    if artist_name in not_indie_list:
        return 0        
    else :
        return indie

# pre-emphasis filter 생성
def preEmpFilter(signal):
    # 맥시마이저 되어있는 소리를 pre-emphasis filter 로 풀어주기
    pre_emphasis = 0.97 # 또는 0.95 0.9357
    return np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])


# 서비스4를 위한 전처리
def Service4(out_path):
    wav_info = {}
    # 0초 ~ 16초 : 최저 4마디 기준
    sound = AudioSegment.from_file(out_path)
    start_time = 0 * 1000
    end_time = (1*17.4) * 1000
    sound = sound[start_time:end_time]
    
    input_wav = out_path[:-4] + '.wav'
    #wav 파일 생성
    sound.export(input_wav, format='wav')

    # signal 뽑기
    _, signal = scipy.io.wavfile.read(input_wav)
    
    # preEmp 필터 통과
    signal = preEmpFilter(signal)
    wav_info = {
    'signal' : signal
    }
    
    # dataframe으로 생성
    df = pd.DataFrame([wav_info])
    
    # 멜스펙트럼으로 바꾸기
    df['signal'] = df['signal'].apply(lambda x : librosa.feature.melspectrogram(y=x, sr=44100//2))
    
    # LSTM input shape에 맞춰서 signal 변환
    df['signal'] = df['signal'].apply(lambda x : np.array(x.T.tolist()))
    
    return df

def paddingData(df):
    data = []
    max_time_steps = 3001
    # (samples, time_steps, features)
    # 샘플 수, 시간, 128
    signal = df.iloc[0]['signal']
    time_steps, features = signal.shape
    # if time_steps > max_time_steps:
    #     max_time_steps = time_steps
    signal = np.expand_dims(signal, axis=0)  # samples=1로 만듦
    data.append(signal)
    samples = len(data)
    features = data[0].shape[2]
    
        
    # 초기화
    X = np.zeros((samples, max_time_steps, features))
    
    # sample만큼 반복
    for k in range(samples):
        # 패딩 작업
        
        time_steps = data[k].shape[1]

        padding_size = max_time_steps - time_steps
        if padding_size > 0:
            padded_signal = np.pad(data[k], ((0, 0), (0, padding_size), (0, 0)), mode='constant')
        else:
            padded_signal = data[k][:,:max_time_steps,:]
        X[k] = padded_signal
        
    return X

async def result(request, id):
    check_ = 0
    # 스포티파이 id, secert 정보
    client_id='baa750d0d8984735b51fa1c31b643d0b'
    client_secret='42347bd6d3f8405188650673a3155594'
    # localhost = "http://localhost:8889/callback"
    # scope = "user-library-read"
    
    # 스포티파이 api 가져오기
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    # 노래 검색
    song = sp.track(id)
    
    # 아티스트 정보
    artist = song['artists']
    artist_spotify_url = song['artists'][0]['external_urls']['spotify']
    artist_id = song['artists'][0]['id']
    artist_info = sp.artist(artist_id)
    
    # 곡 정보
    artist_name = song['artists'][0]['name']
    song_name = song['name']
    # print(artist_name,song_name)

    # 이미지 파일
    album_img = song['album']['images'][1]['url']
    artist_img = artist_info['images'][1]['url']
    
    # service용 곡 정보 가져오기
    song_popularity = song['popularity']
    artist_popularity = artist_info['popularity']
    genres = artist_info['genres']
    followers = artist_info['followers']['total']
    
    # genres 전처리
    genres = genreList(genres)
    genres = changeGenres(genres)
    
    # 년도 찾기
    years_ = int(song['album']['release_date'].split('-')[0])
    
    if years_ >= 2021 :
        years = 1
    elif years_ >= 2019 :
        years = 2
    elif years_ >= 2017 :
        years = 3
    elif years_ >= 2015 :
        years = 4    
    elif years_ >= 2010 :
        years = 5 
    elif years_ >= 2000 :
        years = 6 
    elif years_ >= 1990 :
        years = 7 
    elif years_ >= 1980 :
        years = 8 
    elif years_ <= 1979 :
        years = 9 
    else :
        years = 10    
        
    # indie 찾기
    indie = findIndie(artist_name)
    if followers <= 300000:
        indie = 1
    indie = checkIndie(artist_name, indie) 

    if indie == 0:
        indie_k = '메이저 출신'
    else :
        indie_k = '인디 출신'
        
    # 30초 미리듣기    
    src=song['preview_url']
    
    # from _ post
    if request.method == 'POST':
        check_ = 1
        gender = request.POST['gender']
        instr_re = request.POST['re_inst']
        bass_type = request.POST['bass_type']
        rhythm = request.POST['rhythm']
        main_instr = request.POST['main_instr']
        english = request.POST['english']
        retro = request.POST['retro']
        lofi = request.POST['lofi']

        try :
            # features
            features = sp.audio_features(tracks=id)
            new_df = pd.DataFrame(features)[['danceability', 'energy', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms']]
            
            # new_df2 생성
            new_dict_sp = {
                'popularity_track':song_popularity,
                'popularity_artist':artist_popularity,
                'followers':followers,
                'genres':genres,
                'years' : years,
                'indie' : indie,
                
                'gender':gender,
                'main_instr':main_instr,
                
                'bass_type' : bass_type,
                'rhythm' : rhythm,
                
                'lofi' : lofi,
                'english' : english,
                'retro' : retro,
                're_inst' : instr_re,
            }
            new_df2 = pd.DataFrame([new_dict_sp])
            new_df2 = pd.concat([new_df,new_df2],axis=1)
            
            # tempo 전처리
            new_df2['tempo'] = new_df2['tempo'].astype(int)
            new_df2['half_tempo_check'] = new_df2[['genres','tempo']].apply(changeTempo,axis=1)
            new_df2 = new_df2.drop(columns=['tempo'])
            
            
            # service_1 
            
            # get_dumies
            new_df3 = pd.get_dummies(new_df2,columns=[
                'bass_type', 
                'english', 'gender',   'indie',
                'main_instr','re_inst', 'retro', 'rhythm','years','lofi',
                
                'genres',
            ])
            # print(new_df3)
            spoti_col = [
            # 'score', 
            'liveness', 'loudness', 'instrumentalness', 'mode',
            'popularity', 'popularity_artist', 'speechiness', 'valence',
            'half_tempo_check', 'duration_ms', 'energy', 'danceability',
            'acousticness', 'followers', 'bass_type_0', 'bass_type_1',
            'bass_type_2', 'bass_type_3', 'bass_type_4', 'english_0', 'english_1',
            'gender_1', 'gender_2', 'gender_3', 'gender_4', 'gender_5', 'gender_6',
            'indie_0', 'indie_1', 'main_instr_0', 'main_instr_1', 'main_instr_4',
            're_inst_0', 're_inst_1', 're_inst_2', 're_inst_3', 're_inst_4',
            're_inst_5', 're_inst_6', 're_inst_7', 're_inst_8', 'retro_0',
            'retro_1', 'rhythm_0', 'rhythm_1', 'rhythm_2', 'rhythm_3', 'rhythm_4',
            'rhythm_5', 'rhythm_6', 'rhythm_7', 'rhythm_8', 'rhythm_9', 'rhythm_10',
            'rhythm_11', 'rhythm_12', 'rhythm_13', 'rhythm_14', 'rhythm_15',
            'rhythm_16', 'rhythm_17', 'rhythm_18', 'years_1', 'years_2', 'years_3',
            'years_4', 'years_5', 'years_6', 'years_7', 'years_8', 'years_9',
            'years_10', 'lofi_0', 'lofi_1', 'genres_black', 'genres_country',
            'genres_dance', 'genres_ect', 'genres_edm', 'genres_funk',
            'genres_indie', 'genres_media', 'genres_newage', 'genres_pop',
            'genres_rap', 'genres_retro', 'genres_rock']
            
            new_df3 = new_df3.reindex(columns=spoti_col, fill_value=0)
            # pd.set_option('display.max_rows', None)
            # pd.set_option('display.max_columns', None)
            # print(new_df3)
            # service_1 model
            model = joblib.load('main\static\models\service1\serrvice_1_spotify_anlys_voting_all.pkl')
            service_1 = model.predict(new_df3)
            
            service_1_k = serviceCheck(service_1)
            # mp3 저장
            # src=song['preview_url']
            out_path = f'main\media\{id}.mp3'   
            
            file = wget.download(src, out=out_path)
            
            
            # service 4
            model4 = tf.keras.models.load_model('main\static\models\service4\end_to_end_final32.h5')
            
            # 전처리
            df4 = Service4(out_path)
            
            # padding
            X4data = paddingData(df4)
            
            service_4 = model4.predict(X4data)
            service_4 = round(service_4[0][0],4)
            
            # 노래 삭제
            os.remove(out_path)
            os.remove(out_path[:-4]+'.wav')
            
            # # 모델 자동 추가 학습
            # if service_4 >= 0.5:
            #     y4data = np.array([1])
            # else :
            #     y4data = np.array([0])
            # model4.fit(X4data, y4data, epochs=10, verbose=2)
            # model4.save('main\static\models\service4\end_to_end_final32.h5')
            
            
            context = {
                'service_1':service_1_k,
                'service_4':service_4,
                'artist_name':artist_name,
                'song_name':song_name,
                'album_img':album_img,
                'artist_img':artist_img,
                'followers':followers,
                'years' : years_,
                'genres': genres,
                'id':id,
                'src':src,
                'check':check_,
                'artist_popularity':artist_popularity,
                'song_popularity':song_popularity,
                'indie_k':indie_k,
                
            }
            
            return render(request, "main/result.html", context=context)
        except TypeError as e:
            print(e)
            service_1_k = '해당 노래는 거주 국가에서 분석이 안되는 노래입니다.'
            check_=1
            context = {
            'id':id,
            'service_1':service_1_k,
            'artist_name':artist_name,
            'song_name':song_name,
            'album_img':album_img,
            'artist_img':artist_img,
            'followers':followers,
            'years' : years_,
            'genres': genres,
            'src':src,
            'check':check_,
            'artist_popularity':artist_popularity,
            'song_popularity':song_popularity,
            'indie_k':indie_k,
            }
            return render(request, "main/result.html", context=context)
    
    context = {
    'id':id,
    'artist_name':artist_name,
    'song_name':song_name,
    'album_img':album_img,
    'artist_img':artist_img,
    'followers':followers,
    'years' : years_,
    'genres': genres,
    'src':src,
    'check':check_,
    'artist_popularity':artist_popularity,
    'song_popularity':song_popularity,
    'indie_k':indie_k,
    }
    return render(request, "main/result.html", context=context)