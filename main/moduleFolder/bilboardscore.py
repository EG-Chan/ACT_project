import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import datetime

class BilBoard:
  
  def __init__(self, df):
    self.df = df
    self.df2 = None
    self.next_tuesday = None
    self.address_list = []
    self.soup_list = []
    self.bb_list = []
    self.d = {}
    
  def nextTuesday(self):
    # today = datetime.date.today() - datetime.timedelta(days=6)
    today = datetime.date.today()
    next_tuesday = today + datetime.timedelta( (1-today.weekday()) % 7 )
    self.next_tuesday = next_tuesday
    
  def collectionWhenChart(self):
    address_list =  [f"https://www.billboard.com/charts/hot-100/{self.next_tuesday}"]
    self.address_list = address_list
    
  def collectionWhatChart(self):
    for _, address in enumerate(self.address_list):
      res = requests.get(address)
      res.encoding = None
  
      self.soup_list.append(bs(res.text))
  
  def collectionDoChart(self):
    for _, soup in enumerate(self.soup_list):
    
      title_list = soup.select('.o-chart-results-list__item > #title-of-a-story')
      artist_list = soup.select('.o-chart-results-list__item > #title-of-a-story + span')
      # rank_list = soup.select('.o-chart-results-list-row-container > ul > li:first-child > span:first-child')

      for i in range(len(title_list)):
          
          self.d["title"] = title_list[i].text.replace("\t","").replace("\n","")
          self.d["artist"] = artist_list[i].text.replace("\t","").replace("\n","")
          # self.d["rank"] = rank_list[i].text.replace("\t","").replace("\n","")
          self.bb_list.append(self.d)
          
  def changeDataFrame(self):
    self.df2 = pd.DataFrame(self.bb_list)
    self.df = pd.concat([self.df,self.df2]).drop_duplicates(ignore_index=True)
    self.df.to_csv('main/static/models/bilboard/bilborad_in_score1.csv',index=False)
    return self.df