# service2, 4 음원 분석 라이브러리
import requests

class Service:

    def __init__(self):
        pass

    # step 2 genres 축양을 위한 리스트화
    def genreList(self, genres):
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
    def changeGenres(self, x):
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


    def findYear(self, years):
        if years>= 2021 :
            years = 1
        elif years >= 2019 :
            years = 2
        elif years >= 2017 :
            years = 3
        elif years >= 2015 :
            years = 4    
        elif years >= 2010 :
            years = 5 
        elif years >= 2000 :
            years = 6 
        elif years >= 1990 :
            years = 7 
        elif years >= 1980 :
            years = 8 
        elif years <= 1979 :
            years = 9 
        else :
            years = 10


    def findIndie(self, artist_name, followers):
        urls = 'https://en.wikipedia.org/wiki/'
        response = requests.get(urls + artist_name)
        indie = None
        if ('indie' in response.text) or ('on TikTok' in response.text) or ('Underground' in response.text) or ('minor hit' in response.text) or \
            ('meme' in response.text) or ('Challenge' in response.text) or ('DJ' in response.text) or ('GYM' in response.text) :
            indie = 1
        else :
            indie = 0
        
        if followers <= 300000:
            indie = 1
        
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
            indie = 0       
        else :
            indie = 1
        
        if indie == 0:
            return "메이저 출신"
        else :
            return "인디 출신"
            
    # tempo 변경
    def changeTempo(self, x):
        if x[0] == 'rap':
            if x[1] >= 120 :
                return x[1] / 2
            else :
                return x[1]
        else :
            return x[1]
        
    def serviceCheck(self, service):
        if 1 in service:
            return '빌보드 가능성 있음'
        else :
            return '빌보드 가능성 거의 없음'
    

    