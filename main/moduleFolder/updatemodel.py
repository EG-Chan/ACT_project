import pandas as pd
import re
import unicodedata
import tensorflow as tf
import numpy as np
class UpdateModel:
  
  def __init__(self, df, title, artist):
    self.df = df
    self.title = title
    self.artist = artist
    self.divpart_title = None
    self.divpart_artist = None
    self.score = 0

  def convertAscii(self):
    title_f = self.title
    artist_f = self.artist
    self.title =  unicodedata.normalize('NFKD', self.title).encode('ascii', 'ignore').decode('ascii')
    self.artist =  unicodedata.normalize('NFKD', self.artist).encode('ascii', 'ignore').decode('ascii')
    if (self.title == '') or (self.artist == ''):
      self.title = title_f
      self.artist = artist_f
  
  def getPartDiv(self):
    
    # 이름을 영어로 변경
    self.convertAscii()

    # 전처리
    pattern_a = r'\(|&|feat|Feat|\+| x |,'
    # print(self.title)
    part_title = self.title.split('(')
    part_artist = re.split(pattern_a, self.artist)
    # print(part_title)
    if not part_title[0] == '':
      self.title = part_title[0]
    else :
      self.title = part_title[1].split(')')[1]
      
    self.artist = part_artist[0]
    
    self.blankDel()
  
  def blankDel(self):
    self.title = self.title.replace(' ', '')
    self.artist = self.artist.replace(' ', '')

  def searchDF(self):
    
    self.getPartDiv()
    
    ## 제목에 욕이 *로 되어있는 것 처리_ 그냥 패스하기(어차피 19에서 걸러짐)    
    # title_list = []
    
    # if '*' in self.title:
    #   title_list = self.title.split('*')
    #   for title_swear in title_list:
    #     if not title_swear=='':
    #       self.df['title'].apply(lambda x: x.replace(' ', '')).str.contains(title_swear, case=False, na=False)
    
    # case : 대소문자 구별X, 공백 제거
    self.divpart_title = self.df['song'].apply(lambda x: x.replace(' ', '')).str.contains(self.title, case=False, na=False)
    self.divpart_artist = self.df['artist'].apply(lambda x: x.replace(' ', '')).str.contains(self.artist, case=False, na=False)
    
    # 겹치는 것이 있는지 체크  
    if (self.divpart_title & self.divpart_artist).any():
      self.score = 1
      # return 1
    else :
      self.score = 0
      # return 0
  
  
  def modelFit(self, X):
    self.searchDF()
    model = tf.keras.models.load_model('main/static/models/service3/end_to_end_final8192.h5')
    model.fit(X, np.array([self.score]), epochs=1, verbose=2)
    model.save('main/static/models/service3/end_to_end_final8192.h5')