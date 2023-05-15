from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
import joblib
import time
import pandas as pd

class Service:

    def __init__(self, data):
        self.title = data["title"]
        self.artist = data["artist"]
        self.comments = 0
        self.likes = 0
        self.views = 0
        self.error = False

    def getData(self):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument('headless')
            wd = webdriver.Chrome(options=options)
            wd.get("https://playboard.co/")
            wd.set_window_size(1200, 900)

            title = self.title
            artist = self.artist
            
            # 해당 동영상으로 접속
            wd.find_element(By.CSS_SELECTOR, 'form > #q').send_keys(title + ' ' + artist)
            wd.find_element(By.CSS_SELECTOR, 'form > #q').send_keys(Keys.RETURN)
            time.sleep(2)
            wd.find_element(By.CSS_SELECTOR, '.lnb__menu > :nth-child(2)').click()
            time.sleep(2)

            wd.find_element(By.CSS_SELECTOR, '.opts .selectbox > .btn').click()
            wd.find_element(By.CSS_SELECTOR, '.selectbox > .popup > .list > li:nth-of-type(4)').click()
            time.sleep(1)

            wd.find_element(By.CSS_SELECTOR, '.videos > div > .list > div:nth-of-type(1) > article > .meta > .title > a > h3').click()
            time.sleep(4)
            
            order = 0
            # 정보 추출하기 (일당 조회수 증가량)
            t_path_list = ['//*[@id="app"]/div[1]/div/main/article/div[5]/div/section/div[2]/div/div/div[1]/div/div/table/tbody',
                        '//*[@id="app"]/div[1]/div/main/article/div[6]/div/section/div[2]/div/div/div[1]/div/div/table/tbody'
                        ]
            views_list = None
            for i in t_path_list:
                try:
                    views_tbody = wd.find_element(By.XPATH, i)
                    views_list = list()
                    
                    for tr in views_tbody.find_elements(By.TAG_NAME, "tr"):
                        temp_dict = dict()
                        temp_dict["date"] = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                        temp_dict["total_views"] = tr.find_elements(By.TAG_NAME, "td")[1].get_attribute("innerText")
                        temp_dict["increase_views"] = tr.find_elements(By.TAG_NAME, "td")[2].get_attribute("innerText")
                        views_list.append(temp_dict)
                    break
                except:
                    order = 1
                    pass
            # 정보 추출하기 (일당 좋아요 댓글 증가량)
            f_path_list = '//*[@id="app"]/div[1]/div/main/article/div[{0}]/div/section/div[2]/div/div/div[1]/div/div/table/tbody'.format(6+order)
            feedback_list = None           
            try:
                feedback_tbody = wd.find_element(By.XPATH, f_path_list)
                feedback_list = list()

                for tr in feedback_tbody.find_elements(By.TAG_NAME, "tr"):
                    temp_dict = dict()
                    temp_dict["date"] = tr.find_elements(By.TAG_NAME, "td")[0].get_attribute("innerText")
                    temp_dict["likes"] = tr.find_elements(By.TAG_NAME, "td")[2].get_attribute("innerText")
                    temp_dict["comments"] = tr.find_elements(By.TAG_NAME, "td")[4].get_attribute("innerText")
                    feedback_list.append(temp_dict)

            except:
                pass

            # view_list에 feedback_list 병합
            for i, data in enumerate (views_list):
                data.update(feedback_list[i])

            print(views_list)
            date = list()
            repeat = 7
            for i in range(repeat):
                s = datetime.today() - timedelta(i)
                date.append(s.strftime("%m-%d"))

            variance_comments = 0
            variance_likes = 0
            variance_views = 0

            for data in views_list:
                if data["date"] in date:
                    variance_comments += int(data["comments"].replace(",", ""))
                    variance_likes += int(data["likes"].replace(",", ""))
                    variance_views += int(data["increase_views"].replace(",", ""))
            self.comments = variance_comments
            self.likes = variance_likes
            self.views = variance_views
            
        except:
            self.error = True
            
        finally:
            wd.quit()
            return {
                "data":{
                    "comments":self.comments,
                    "likes":self.likes,
                    "views":self.views,
                },
                "error":self.error
            }
    
    def runModel(self, data):
        dataFrame = pd.DataFrame([data["data"]])
        model = joblib.load('static/models/service2/serrvice_2_issue_all.pkl')
        result = model.predict(dataFrame)
        
        if result[0] == 0:
            data["result"] = "가능성 없음"
        else:
            data["result"] = "가능성 있음"

        return data