import tensorflow as tf
from tensorflow import keras
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import VotingClassifier
from sklearn.preprocessing import MinMaxScaler

from spleeter.separator import Separator
import os
from pydub import AudioSegment
import matplotlib.pyplot as plt
import scipy.io.wavfile
from scipy.fftpack import dct
import librosa
import librosa.display
import matplotlib.pyplot as plt
import matplotlib as mpl
import math
import time
import datetime
import pickle
import cmath
import wget

class oneClick:
  def __init__(self, id, src, title='test', artist='test'):
    self.df = None
    self.id = id
    self.track_src = src
    self.signal = None
    self.title = title
    self.artist = artist
    self.output_path = f'media\{self.id}.mp3' 
    self.input_wav = None
    self.folder_4stem_list = []
    self.output_4stem_path = f'media/{self.title}__{self.artist}/{self.title}__{self.artist}'
    self.models = []
    self.t_model = ()
    self.df_col = None
    oneClick().__init__()
    
  def preEmpFilter(self):
    # 맥시마이저 되어있는 소리를 pre-emphasis filter 로 풀어주기
    pre_emphasis = 0.97 # 또는 0.95 0.9357
    return np.append(self.signal[0], self.signal[1:] - pre_emphasis * self.signal[:-1])

  def melSignal(self):
    i=0
    # 사람들의 가청 주파수 최저치 20Hz를 최대 주기로 잡을 수 있게 (하나의 특징으로) 데이터를 순간으로 나눔
    while i <= (len(self.df['signal'].loc[0])*20//88200) :
        self.df[f'signal_{i}'] = self.df['signal'].apply(lambda x : x[(i*88200//20):((i+1)*88200//20)])
        i+=1
    return self.df

  def lastLenDel(x):
    if len(x) != 1411200:
        return None
    else :
        return x
      
  def libAmplitudeTodB(x):
    return librosa.feature.melspectrogram(y=x, sr=44100*2)    

  def AmplitudeTodB2(x):
    # 사람 귀를 기준으로 우선 바꾸기, 음악 n_fft =2048, 음성:512
    y = librosa.feature.melspectrogram(y=x, sr=44100*2, n_fft=2048) 
    return librosa.amplitude_to_db(y, ref=np.max)

  # [0] tempo, [1] beat
  def predTempo(x):
    return librosa.beat.beat_track(y=x, sr=44100*2)[0]

  # 1만 주기 평균
  def cycleFunction(x):
    try:
        y = np.array([i for i in x if i!= 0])
        return (1 / librosa.feature.spectral_centroid(y=y, sr=44100*2)[0]).mean()*10000    
    except :
        # 최악의 경우 계산시 696.598, inf이면 700으로 두기
        return 0

  # 1만 주기 평균
  def cycleVar(x):
    try :
        y = np.array([i for i in x if i!= 0])
        return np.var((1 / librosa.feature.spectral_centroid(y=y, sr=44100*2)[0]))*(10**8)   
    except :
        # 소리가 안나는 경우는 변화가 없으므로 0
        return 0

  # 시작 위치 탐색
  def startMusic(x):
    start_list=[]
    y = librosa.onset.onset_strength(y=x, sr=(44100*2))
    for i in y:
        if i==0:
            start_list.append(i)
        else :
            break
    # 0.005초 보다 많이 비면 시작으로 탐색
    if len(start_list)>=2:
        # len()/127.3125 : 1초
        return len(start_list)/127.3125
    else :
        return 0
  
  def stem4folder(self):
    for path_out_4stem in os.listdir(self.output_4stem_path):
      self.folder_4stem_list.append(path_out_4stem)
  
  def oneClick(self):
    
    self.Stem4()
    self.stem4folder()
    self.folder_4stem_list.append(None)
    for divide in self.folder_4stem_list:
      self.createDataFrame(out4stem=divide)
    
      self.df['predTempo'] = self.df['signal'].apply(self.predTempo)
      self.df['stft_mean'] = self.df['signal'].apply(lambda x : librosa.stft(x).mean())
      self.df['stft_var'] = self.df['signal'].apply(lambda x : np.var(librosa.stft(x)))
      self.df['amplitude_to_db'] = self.df['signal'].apply(self.AmplitudeTodB2)
      self.df['amplitude_to_db_BL'] = self.df['amplitude_to_db'].apply(lambda x : x[:7].mean())
      self.df['amplitude_to_db_ML'] = self.df['amplitude_to_db'].apply(lambda x : x[5:20].mean())
      self.df['amplitude_to_db_HL'] = self.df['amplitude_to_db'].apply(lambda x : x[18:50].mean())
      self.df['amplitude_to_db_SHL'] = self.df['amplitude_to_db'].apply(lambda x : x[48:].mean())
      # 소리가 음->양 or 양->음 변화 횟수의 합
      self.df['zero_crossings'] = self.df['signal'].apply(lambda x : sum(librosa.zero_crossings(x, pad=False)))
      # 고조파, 기본 주파수
      # self.df['h_r_vector'] = self.df['signal'].apply(lambda x : librosa.effects.hpss(x))
      # self.df['perc'] = self.df['h_r_vector'].apply(lambda x : x[1])
      # self.df['harmonic'] = self.df['h_r_vector'].apply(lambda x : x[0])
      self.df['harmonic'] = self.df['signal'].apply(lambda x : librosa.effects.hpss(x))
      self.df['perc'] = self.df['harmonic'].apply(lambda x : x[1])
      self.df['harmonic'] = self.df['harmonic'].apply(lambda x : x[0])
      # 하모닉, 진동폭 평균
      self.df['harmonic_rms_mean'] = self.df['harmonic'].apply(lambda x : librosa.feature.rms(y=x).mean())
      self.df['harmonic_rms_var'] = self.df['harmonic'].apply(lambda x : np.var(librosa.feature.rms(y=x)))
      # 하모닉, 주기 평균 * 10000 (10000주기 평균)
      self.df['harmonic_cycle_mean'] = self.df['harmonic'].apply(self.cycleFunction)
      # 하모닉, 주기 평균 * 10000 (10000주기 평균)
      self.df['harmonic_cycle_var'] = self.df['harmonic'].apply(self.cycleVar)
      # 타악기, 주파수 정수배 X

      # self.df['perc'] = self.df['signal'].apply(lambda x : librosa.effects.hpss(x)[1])
      # 타악기, 주파수 정수배 X, 진동폭 평균
      self.df['perc_rms_mean'] = self.df['perc'].apply(lambda x : librosa.feature.rms(y=x).mean())
      # 타악기, 주파수 정수배 X, 진동폭 분산
      self.df['perc_rms_var'] = self.df['perc'].apply(lambda x : np.var(librosa.feature.rms(y=x)))
      # 타악기, 주파수 정수배 X, 주기 평균 * 10000 (10000주기 평균)
      self.df['perc_cycle_mean'] = self.df['perc'].apply(self.cycleFunction)
      # 타악기, 주파수 정수배 X, 주기 분산 * 10000^2 (10000주기 분산)
      self.df['perc_cycle_var'] = self.df['perc'].apply(self.cycleVar)


      # spectral centroid mean, 소리의 무게중심 평균 찾기 
      # 곡 전체를 토대로 분석해서 사용하는 것이 맞지만, 4마디 or 8마디에도 기승 전결로 3마디 타이밍(6마디)에 치고나오는 소리가 있기에 필요한 데이터라고 판단
      self.df['spectral_centroid_mean'] = self.df['signal'].apply(lambda x : librosa.feature.spectral_centroid(y=x, sr=(44100*2))[0].mean())
      # spectral centroid var, 무게중심 분산 구하기
      self.df['spectral_centroid_var'] = self.df['signal'].apply(lambda x : np.var(librosa.feature.spectral_centroid(y=x, sr=(44100*2))[0]))
      # spectral bandwidth mean, 소리의 대역폭 평균
      self.df['spectral_bandwidth_mean'] = self.df['signal'].apply(lambda x : librosa.feature.spectral_bandwidth(y=x, sr=(44100*2))[0].mean())
      # spectral bandwidth var, 소리의 대역폭 분산
      self.df['spectral_bandwidth_var'] = self.df['signal'].apply(lambda x : np.var(librosa.feature.spectral_bandwidth(y=x, sr=(44100*2))[0]))
      self.df['spectral_rolloff_mean'] = self.df['signal']\
          .apply(lambda x : librosa.feature.spectral_rolloff(y=x, sr=(44100*2), roll_percent=0.85).mean())
      self.df['spectral_rolloff_var'] = self.df['signal']\
          .apply(lambda x : np.var(librosa.feature.spectral_rolloff(y=x, sr=(44100*2), roll_percent=0.85)))
      # rms 평균, 분산 구하기
      # self.df['rms_mean'] = self.df['signal'].apply(lambda x : librosa.feature.rms(y=x).mean())
      self.df['rms_var'] = self.df['signal'].apply(lambda x : np.var(librosa.feature.rms(y=x)))
      # 주기 평균, 분산 구하기
      # self.df['cycle_mean'] = self.df['signal'].apply(cycleFunction)
      # self.df['cycle_var'] = self.df['signal'].apply(cycleVar)
      # Chroma Frequencies 화음 인식
      self.df['chromagram_mean'] = self.df['signal']\
          .apply(lambda x : librosa.feature.chroma_stft(y=x, sr=44100*2, hop_length=512).mean())
      # Chroma Frequencies 화음 인식
      self.df['chromagram_var'] = self.df['signal']\
          .apply(lambda x : np.var(librosa.feature.chroma_stft(y=x, sr=44100*2, hop_length=512)))
      # self.df['start_time'] = self.df['signal'].apply(startMusic)
      self.df['MFCCs_vector'] = self.df['signal'].apply(lambda x : librosa.feature.mfcc(y=x, sr=44100*2))
      self.df['MFCC_mean'] = self.df['MFCCs_vector'].apply(lambda x : x.mean())
      self.df['MFCC_var'] = self.df['MFCCs_vector'].apply(lambda x : np.var(x))
      # self.df['lpc_coeffs_mean'] = self.df['signal'].apply(lambda x : librosa.lpc(y=x, order=16))
      self.preChange()
  
  def createDataFrame(self, out4stem=None):
    wget.download(self.track_src, out=self.output_path)
    wav_info = {}
    sound = AudioSegment.from_file(self.output_path)
    self.input_wav = self.output_path[:-4] + '.wav'
    if out4stem==None:
      sound.export(self.input_wav, format='wav')
      _, signal = scipy.io.wavfile.read(self.input_wav)
      wav_info = {
        'signal' : signal
      }
      self.df = pd.DataFrame([wav_info])
    else :
      wavfile = self.output_4stem_path +'/' + out4stem
      sound.export(wavfile, format='wav')
      _, signal = scipy.io.wavfile.read(self.input_wav)
      wav_info = {
      'signal' : signal
      }
      self.df = pd.DataFrame([wav_info])
  
  def preChange(self):
    self.df = self.df[[
              'title','artist',
              # 'signal', 
              # 'predTempo', 
              'stft_mean', 'stft_var',
              # 'amplitude_to_db', 
              'amplitude_to_db_BL', 'amplitude_to_db_ML',
              'amplitude_to_db_HL', 'amplitude_to_db_SHL', 'zero_crossings',

              # 'harmonic', 'perc', 

              'harmonic_rms_mean', 'harmonic_rms_var',
              'harmonic_cycle_mean', 'harmonic_cycle_var', 'perc_rms_mean',
              # 'perc_rms_var', 
              'perc_cycle_mean', 
              # 'perc_cycle_var',
              'spectral_centroid_mean', 'spectral_centroid_var',
              'spectral_bandwidth_mean', 'spectral_bandwidth_var',
              'spectral_rolloff_mean', 'spectral_rolloff_var', 
              # 'rms_mean', 
              'rms_var',
              # 'cycle_mean', 'cycle_var', 
              'chromagram_mean', 'chromagram_var',
              'start_time', 
              # 'MFCCs_vector', 
              'MFCC_mean', 'MFCC_var',

              # 'score'
              ]]
    # 전처리 해주기
    
    ## harmonic_cycle_mean : inf 제거, 즉 소리 0 제거, harmonic_cycle_var : nan 이면 제거
    # df = df[~df['harmonic_cycle_var'].isnull()].reset_index().drop(columns=['index'])
    
    # 복소수 실수화
    self.df['stft_mean'] = self.df['stft_mean'].apply(cmath.phase)
    
    # 시작 유무 체크
    # df['start_time'] = df['start_time'].apply(lambda x : 1 if x != 0 else 0)
  
  # 4stem 분리
  def Stem4(self):
    separator = Separator('spleeter:4stems')
    separator.separate_to_file(self.input_wav, f'media/{self.title}__{self.artist}')

  # model 가져오기
  def takeModel(self):
    path = 'main/static/models/service4'
    for path_folder in os.listdir(path):
      for path_file in os.listdir(path + '/' + path_folder):
        new_path = path + '/' + path_folder + '/' + path_file
        model = keras.models.load_model(new_path)
        name = f'{path_folder}_{path_file}'
        name = name[:-3]
        self.t_model = (name,model)
        self.models.append(self.t_model)
  
  # 학습 데이터
  def splitDfKF(self, Scaler=MinMaxScaler):
      
      # 정규화
      scaler = Scaler(feature_range=(0, 1))
      self.X = scaler.fit_transform(self.X)
      # 3차원 맞추기
      self.X = np.reshape(self.X, (self.X.shape[0], self.X.shape[1], 1))
      
      return self.X, scaler
  
  # 최종 모델
  def votingModel(self):
    self.takeModel()
    self.splitDfKF()
    soft_voting = VotingClassifier(estimators=self.models, voting = 'soft')
    y_pred = soft_voting.predict(self.X)
    return y_pred

  def scoreBy4(self, y_pred):
    y_finals = [] 
    pred_list=[]
    pred_list.append(y_pred)
    y_pred_final = np.mean(pred_list, axis=0)
    y_pred_final_mean = np.mean(y_pred_final, axis=1)
    for y_f in y_pred_final_mean:
        if y_f > 0.5 :
            y_finals.append(1)
        else :
            y_finals.append(0)
    # accuracy = accuracy_score(y_test, y_finals)
    # print(accuracy)
    score = {x: y_finals.count(x) for x in y_finals}
    percent = round(score[1]/(score[1]+score[0]),2)
    if percent > 0.5 :
      return '빌보드 가능성 높음'
    else :
      return '빌보드 가능성 낮음'
