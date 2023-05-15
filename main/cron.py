from main.moduleFolder import bilboardscore as bbs
import pandas as pd

df = pd.read_csv('main/static/models/bilboard/bilborad_in_score1.csv')
# print(df)
def tuesdayBilboard(df):
  bb = bbs.BilBoard(df)
  bb.nextTuesday()
  bb.collectionWhenChart()
  bb.collectionWhatChart()
  bb.collectionDoChart()
  df = bb.changeDataFrame(df)
  return df


df = tuesdayBilboard(df)

# python manage.py crontab add 터미널 창에 입력하면 테스트 가능