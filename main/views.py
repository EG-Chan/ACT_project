from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

#사용자 정보 저장
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

#사용자 모듈 불러오기
from main.moduleFolder import service01 as s1
from main.moduleFolder import service02 as s2
from main.moduleFolder import service03 as s3

import tensorflow as tf

# 스포티파이 id, secert 정보
client_id = "baa750d0d8984735b51fa1c31b643d0b"
client_secret = "42347bd6d3f8405188650673a3155594"

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

        client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        artist = sp.search(q=f'{search}', type='track')

        return render(request, "main/search.html", {"spotipyDatas":artist})
    return render(request, "main/search.html")



def result(request, id):
    service01 = s1.Service()
    service03 = s3.Service()

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

    # 이미지 파일
    album_img = song['album']['images'][1]['url']
    artist_img = artist_info['images'][1]['url']
    
    # service용 곡 정보 가져오기
    song_popularity = song['popularity']
    artist_popularity = artist_info['popularity']
    genres = artist_info['genres']
    followers = artist_info['followers']['total']
    
    check_ = 0

    # genres 전처리
    genres = service01.genreList(genres)
    genres = service01.changeGenres(genres)
    
    # 년도 찾기
    years = service01.findYear(int(song['album']['release_date'].split('-')[0]))
    
    # indie 찾기
    indie = service01.findIndie(artist_name, followers)
        
    # 30초 미리듣기    
    src = song['preview_url']
    if request.method == "GET":

        context = {
            'id':id,
            'artist_name':artist_name,
            'song_name':song_name,
            'album_img':album_img,
            'artist_img':artist_img,
            'followers':followers,
            'years' : years,
            'genres': genres,
            'src':src,
            'check':check_,
            'artist_popularity':artist_popularity,
            'song_popularity':song_popularity,
            'indie_k':indie,
        }
        return render(request, "main/result.html", context=context)
    elif request.method == 'POST':
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
            new_df2['half_tempo_check'] = new_df2[['genres','tempo']].apply(service01.changeTempo,axis=1)
            new_df2 = new_df2.drop(columns=['tempo'])
            
            
            # service_1 
            
            # get_dumies
            new_df3 = pd.get_dummies(new_df2,columns=[
                'bass_type', 
                'english', 'gender',   'indie',
                'main_instr','re_inst', 'retro', 'rhythm','years','lofi',
                
                'genres',
            ])

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
            
            service_1_k = service01.serviceCheck(service_1)
            # mp3 저장
            # src=song['preview_url']
            out_path = f'media\{id}.mp3'   
            
            wget.download(src, out=out_path)
            
            # service 3
            model3 = tf.keras.models.load_model('main\static\models\service3\end_to_end_final32.h5')
            
            # 전처리
            df4 = service03.Service(out_path)
            
            # padding
            X4data = service03.paddingData(df4)
            
            service_4 = model3.predict(X4data)
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
                'years' : years,
                'genres': genres,
                'id':id,
                'src':src,
                'check':check_,
                'artist_popularity':artist_popularity,
                'song_popularity':song_popularity,
                'indie_k':indie,
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
                'years' : years,
                'genres': genres,
                'src':src,
                'check':check_,
                'artist_popularity':artist_popularity,
                'song_popularity':song_popularity,
                'indie_k':indie,
            }
            return render(request, "main/result.html", context=context)
    