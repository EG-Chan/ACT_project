#일단 내가 뭘 쓸지 몰라서 다 가져옴
import pandas as pd
import numpy as np

import sklearn
# from sklearn import preprocessing
# from sklearn.model_selection import train_test_split




import keras
from tensorflow import keras
import tensorflow as tf


import os
import warnings
warnings.filterwarnings('ignore')

import pickle

import joblib

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

# 함수
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

# step 2 genres 축양을 위한 리스트화


def genresDiv(genres):
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
    return genre_list

# # dict 파일 맞춰서 genres2 수정
# for i in all_genres_dict:
#     for j in all_genres_dict[i]:
#         for o in df_new.index:
#             for idx, k in enumerate(df_new.loc[o, 'genres2']):
#                 # print(df.loc[o, 'genres2'], idx, k,j)
#                 if k == j :
#                     # genres3_list.append(i)
#                     # print(k, j,'->', i, o ,'data', idx,'번째',genres3_list)
#                     df_new.loc[o, 'genres2'][idx] = i

def changeTempo(x):
    if x[0] == 'rap':
        if x[1] >= 120 :
            return x[1] / 2
        else :
            return x[1]
    else :
        return x[1]


# 초기화 세팅

# df2_col_ = [
#   'score', 'liveness', 'loudness', 'instrumentalness', 'mode',
#   'popularity', 'popularity_artist', 'speechiness', 'valence',
#   'half_tempo_check', 'duration_ms', 'energy', 'danceability',
#   'acousticness', 'followers', 'bass_type_0', 'bass_type_1',
#   'bass_type_2', 'bass_type_3', 'bass_type_4', 'english_0', 'english_1',
#   'gender_1', 'gender_2', 'gender_3', 'gender_4', 'gender_5', 'gender_6',
#   'indie_0', 'indie_1', 'main_instr_0', 'main_instr_1', 'main_instr_4',
#   're_inst_0', 're_inst_1', 're_inst_2', 're_inst_3', 're_inst_4',
#   're_inst_5', 're_inst_6', 're_inst_7', 're_inst_8', 'retro_0',
#   'retro_1', 'rhythm_0', 'rhythm_1', 'rhythm_2', 'rhythm_3', 'rhythm_4',
#   'rhythm_5', 'rhythm_6', 'rhythm_7', 'rhythm_8', 'rhythm_9', 'rhythm_10',
#   'rhythm_11', 'rhythm_12', 'rhythm_13', 'rhythm_14', 'rhythm_15',
#   'rhythm_16', 'rhythm_17', 'rhythm_18', 'years_1', 'years_2', 'years_3',
#   'years_4', 'years_5', 'years_6', 'years_7', 'years_8', 'years_9',
#   'years_10', 'lofi_0', 'lofi_1', 'genres_black', 'genres_country',
#   'genres_dance', 'genres_ect', 'genres_edm', 'genres_funk',
#   'genres_indie', 'genres_media', 'genres_newage', 'genres_pop',
#   'genres_rap', 'genres_retro', 'genres_rock'
# ]
new_dict_sp = {}


# 실행파일

track_name = ''
artist_name = ''

# 카테고리 줘서 선택하게 끔 해주기
gender = ''
instr_re = ''
main_instr = ''
indie = ''
bass_type = ''
rhythm = ''
years = ''
retro = ''
english = ''
lofi = ''

# 스포티파이 id, secert 정보
client_id=''
client_secret=''
localhost = "http://localhost:8889/callback"
scope = "user-library-read"

# 스포티파이 api 가져오기
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

song = sp.search(q=f'track:{track_name} artist:{artist_name}', type='track')
artist = sp.search(q=f'artist:{artist_name}', type='artist')

followers = artist['artists']['items'][0]['followers']['total']

popularity_track = song['tracks']['items'][0]['popularity']
popularity_artist = artist['artists']['items'][0]['popularity']
features = sp.audio_features(tracks=[song['tracks']['items'][0]['id']])
genres = artist['artists']['items'][0]['genres']

# 중복장르 제거
genre_list = genresDiv(genres)
genre_list = list(set(genre_list))
genres = changeGenres(genre_list)

# dict 형태로 저장
new_dict_sp = {
    'popularity_track':popularity_track,
    'popularity_artist':popularity_artist,
    'followers':followers,
    'genres':genres,
    'gender':gender,
    'instr_re':instr_re,
    'main_instr':main_instr,
    'indie' : indie,
    'bass_type' : bass_type,
    'rhythm' : rhythm,
    'years' : years,
    'lofi' : lofi,
    'english' : english,
    'retro' : retro,
    're_inst' : instr_re,
}

# feature 중 필요한 애만 가져오기
new_df = pd.DataFrame(features)[['danceability', 'energy', 'loudness', 'mode', 'speechiness',
      'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
      'duration_ms']]

# 데이터프레임 만들기
new_df2 = pd.DataFrame([new_dict_sp])
new_df2 = pd.concat([new_df,new_df2],axis=1)

new_df2['tempo'] = new_df2['tempo'].astype(int)

# 장르가 rap인 경우 조건에 따라 half 주기
new_df2['half_tempo_check'] = new_df2[['genres','tempo']].apply(changeTempo,axis=1)
new_df2 = new_df2.drop(columns=['tempo'])

# one_hot_encoding
new_df2 = pd.get_dummies(new_df2,columns=[
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

new_df2 = new_df2.reindex(columns=spoti_col, fill_value=0)


# 모델 가져오기

model = joblib.load('./models/service1/serrvice_1_spotify_anlys_stacking_all.pkl')

# 모델 predict
pred = model.predict(new_df2)