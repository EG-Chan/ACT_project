import requests
import pandas as pd
import joblib

#스포티파이 데이터로 분석
class Service:

    def __init__(self, id):
        self.id = id
        self.track = None
        self.track_name = None
        self.track_genres = None
        self.track_popularity = None
        self.track_img = None
        self.track_year = None
        self.track_date = None
        self.track_src = None
        self.artist = None
        self.artist_name = None
        self.artist_id = None
        self.artist_spotify_url = None
        self.artist_popularity = None
        self.artist_img = None
        self.artist_followers = None
        self.artist_indie = None
        self.dataFrame = None
        
    
    def setMusicInfo(self, track, artist):
        self.track = track
        self.artist = artist

        self.artist_name = track['artists'][0]['name']
        self.artist_id = track['artists'][0]['id']
        self.artist_spotify_url = track['artists'][0]['external_urls']['spotify']
        self.track_name = track['name']
        self.track_popularity = track['popularity']
        self.track_img = track['album']['images'][1]['url']
        self.track_date = track['album']['release_date']
        self.track_year = int(track['album']['release_date'].split('-')[0])
        self.track_src = track['preview_url']

        self.artist_popularity = artist['popularity']
        self.track_genres = artist['genres']
        self.artist_followers = artist['followers']['total']
        self.artist_img = artist['images'][1]['url']
        
        
        self.changeGenres()
        self.findYear()
        self.findIndie()

    def getMusicInfo(self):
        return {
            "id" : self.id,
            "track_name" : self.track_name,
            "track_genres" : self.track_genres,
            "track_popularity" : self.track_popularity,
            "track_img" : self.track_img,
            "track_date" : self.track_date,
            "track_src" : self.track_src,
            "artist_name" : self.artist_name,
            "artist_id" : self.artist_id,
            "artist_spotify_url" : self.artist_spotify_url,
            "artist_popularity" : self.artist_popularity,
            "artist_img" : self.artist_img,
            "artist_followers" : self.artist_followers,
            "artist_indie" : self.artist_indie,
        }
    # 장르 최소화
    def changeGenres(self):
        genre_list = []
        # 장르별 조건 주기
        for i in self.track_genres:
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
        genre_list = list(set(genre_list))

        if 'ect' in genre_list:
            self.track_genres = 'ect'
        elif 'indie' in genre_list:
            self.track_genres = 'indie'
        elif 'world' in genre_list:
            self.track_genres = 'world'
        elif 'rock' in genre_list:
            self.track_genres = 'rock'
        elif 'funk' in genre_list:
            self.track_genres = 'funk'
        elif 'retro' in genre_list:
            self.track_genres = 'retro'
        elif 'dance' in genre_list:
            self.track_genres = 'dance'
        elif 'media' in genre_list:
            self.track_genres = 'media'
        elif 'relax' in genre_list:
            self.track_genres = 'relax'
        elif 'edm' in genre_list or 'house' in genre_list or 'syns' in genre_list:
            self.track_genres = 'edm'
        elif 'black' in genre_list or 'rnb' in genre_list:
            self.track_genres = 'black'
        elif 'country' in genre_list:
            self.track_genres = 'country'
        elif 'newage' in genre_list:
            self.track_genres = 'newage'
        elif 'rap' in genre_list:
            self.track_genres = 'rap'
        else : 
            # 여기에도 없는 태그일 경우 그냥 전부 pop으로 보기
            self.track_genres = 'pop'

    def findYear(self):
        if self.track_year>= 2021 :
            self.track_year = 1
        elif self.track_year >= 2019 :
            self.track_year = 2
        elif self.track_year >= 2017 :
            self.track_year = 3
        elif self.track_year >= 2015 :
            self.track_year = 4    
        elif self.track_year >= 2010 :
            self.track_year = 5 
        elif self.track_year >= 2000 :
            self.track_year = 6 
        elif self.track_year >= 1990 :
            self.track_year = 7 
        elif self.track_year >= 1980 :
            self.track_year = 8 
        elif self.track_year <= 1979 :
            self.track_year = 9 
        else :
            self.track_year = 10


    def findIndie(self):
        urls = 'https://en.wikipedia.org/wiki/'
        response = requests.get(urls + self.artist_name)
        indie = None
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

        indie_wiki_list = ["indie", "on TikTok", "Underground", "minor hit", "meme", "Challenge", "DJ", "GYM"]
        for i in indie_wiki_list:
            if i in response.text:
                indie = 1
                break
            else:
                indie = 0

        if self.artist_followers <= 300000:
            indie = 1

        if self.artist_name in not_indie_list:
            indie = 0

        self.artist_indie = indie
    
    def createDataFrame(self, audio_features, post_data):
        df1 = pd.DataFrame(audio_features)[['danceability', 'energy', 'loudness', 'mode', 'speechiness', 
                                            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 
                                            'duration_ms']]
        
        new_dict_sp = {
            'popularity_track' : self.track_popularity,
            'popularity_artist': self.artist_popularity,
            'followers': self.artist_followers,
            'genres': self.track_genres,
            'years' : self.track_year,
            'indie' : self.artist_indie,
            'gender': post_data["gender"],
            'main_instr': post_data["main_instr"],
            'bass_type' : post_data["bass_type"],
            'rhythm' : post_data["rhythm"],
            'lofi' : post_data["lofi"],
            'english' : post_data["english"],
            'retro' : post_data["retro"],
            're_inst' : post_data["re_inst"],
        }

        df2 = pd.DataFrame([new_dict_sp])
        concat_df = pd.concat([df1, df2],axis=1)

        # tempo 전처리
        concat_df['tempo'] = concat_df['tempo'].astype(int)
        concat_df['half_tempo_check'] = concat_df[['genres','tempo']].apply(self.changeTempo,axis=1)
        concat_df = concat_df.drop(columns=['tempo'])

        df3 = pd.get_dummies(concat_df, columns=[
            'bass_type', 'english', 'gender', 'indie', 'main_instr',
            're_inst', 'retro', 'rhythm', 'years', 'lofi',
            'genres',
        ])

        spoti_col = [
            # 'score', 
            'liveness', 'loudness', 'instrumentalness', 'mode', 'popularity', 
            'popularity_artist', 'speechiness', 'valence', 'half_tempo_check', 
            'duration_ms', 'energy', 'danceability', 'acousticness', 'followers', 
            'bass_type_0', 'bass_type_1', 'bass_type_2', 'bass_type_3', 'bass_type_4',
            'english_0', 'english_1',
            'gender_1', 'gender_2', 'gender_3', 'gender_4', 'gender_5', 'gender_6',
            'indie_0', 'indie_1',
            'main_instr_0', 'main_instr_1', 'main_instr_4',
            're_inst_0', 're_inst_1', 're_inst_2', 're_inst_3', 're_inst_4', 're_inst_5', 're_inst_6', 're_inst_7', 're_inst_8',
            'retro_0', 'retro_1',
            'rhythm_0', 'rhythm_1', 'rhythm_2', 'rhythm_3', 'rhythm_4',
            'rhythm_5', 'rhythm_6', 'rhythm_7', 'rhythm_8', 'rhythm_9',
            'rhythm_10', 'rhythm_11', 'rhythm_12', 'rhythm_13', 'rhythm_14',
            'rhythm_15', 'rhythm_16', 'rhythm_17', 'rhythm_18', 
            'years_1', 'years_2', 'years_3', 'years_4', 'years_5',
            'years_6', 'years_7', 'years_8', 'years_9', 'years_10', 
            'lofi_0', 'lofi_1', 
            'genres_black', 'genres_country', 'genres_dance', 'genres_ect', 'genres_edm',
            'genres_funk', 'genres_indie', 'genres_media', 'genres_newage', 'genres_pop',
            'genres_rap', 'genres_retro', 'genres_rock',
        ]

        self.dataFrame = df3.reindex(columns=spoti_col, fill_value=0)

    # tempo 변경
    def changeTempo(self, x):
        if x[0] == 'rap':
            if x[1] >= 120 :
                return x[1] / 2
            else :
                return x[1]
        else :
            return x[1]
    
    def runModel(self):
        model = joblib.load('main\\static\\models\\service1\\serrvice_1_spotify_anlys_voting_all.pkl')
        result = model.predict(self.dataFrame)

        if 1 in result:
            return '빌보드 가능성 있음'
        else :
            return '빌보드 가능성 거의 없음'
        
        
    def getindie(self):
        if self.artist_indie == 0:
            return "메이저 출신"
        else :
            return "인디 출신"

    