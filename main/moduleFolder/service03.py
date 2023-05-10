from scipy.fftpack import dct
from pydub import AudioSegment

import librosa
import tensorflow as tf
import scipy.io.wavfile
import numpy as np
import pandas as pd

class Service:
    def __init__(self):
        pass


    # 서비스4를 위한 전처리
    def Service(self, out_path):
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
        pre_emphasis = 0.97 # 또는 0.95 0.9357
        signal = np.append(signal[0], signal[1:] - pre_emphasis * signal[:-1])
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

    def paddingData(self, df):
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