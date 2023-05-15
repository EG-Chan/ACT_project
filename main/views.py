from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator

#사용자 정보 저장
from datetime import datetime
import hashlib

#모델
from main.models import Account, SearchHistory

# 
import re

#사용자 모듈 불러오기
from main.moduleFolder import service01 as s1
from main.moduleFolder import service02 as s2
from main.moduleFolder import service03 as s3
from main.moduleFolder import spoti

sp = spoti.Spoti().getSpotiData()

def main(request):
    if request.method == "GET":
        return render(request, "main/main.html")

    elif request.method == "POST":
        pass
    


def login(request):
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
                if not request.session.session_key:
                    request.session.create()
                request.session["email"] = email
                request.session["userName"] = user.name

                session_id = request.session.session_key
                context = {
                    "sessionID" : session_id,
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
            user = Account.objects.get(email=email)
            context = {"state" : 3}
        except Account.DoesNotExist as e:
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
            context = {'state' : 1}
        except:
            context = {"state" : 2}
        finally:
            return render(request, "main/signup.html", context=context)
        
def searchHistory(user_id):
    search_history = SearchHistory.objects.filter(user_id=user_id).order_by('-timestamp')[:10]
    return search_history

def userInfo(request):
    artists=[]
    track_imgs=[]
    track_names=[]
    track_dates=[]
    track_previews=[]
    idxs = []

    try:
        if not request.session.session_key:
            return HttpResponse("<script>alert('세션이 만료되었습니다.');window.location.assign('/login');</script>")
        elif request.session.session_key:
            user = Account.objects.get(email=request.session["email"])
            history = searchHistory(user)
            for idx, data in enumerate(history):
                track = sp.track(data.query)
                artist = track['album']['artists'][0]['name']
                track_img = track['album']['images'][1]['url']
                track_name = track['name']
                track_date = track['album']['release_date']
                track_preview = track['preview_url']
                
                track_dates.append(track_date)
                track_names.append(track_name)
                track_imgs.append(track_img)
                track_previews.append(track_preview)
                artists.append(artist)
                idxs.append(idx)
            history_list = zip(idxs, history, track_names,track_imgs,track_dates, artists,track_previews)
            context = {
                'user':user,
                'history':history_list,
                'session_id' : request.session.session_key,
            }
            return render(request, "main/userInfo.html", context=context)
    except ValueError as e :
        print(e)
        return HttpResponse("<script>alert('세션이 올바르지 않습니다.');window.location.assign('/login');</script>")

def changeInfo(request):
    password = request.POST.get("pw_name")
    email = request.POST.get("email")
    pattern = r'^[a-zA-Z0-9]{6,16}$'
    if not request.session.session_key:
        return HttpResponse("<script>alert('세션이 만료되었습니다.');window.location.assign('/login');</script>")
    else :
        if password == '':
            return HttpResponse("<script>alert('비밀번호를 입력해주세요..');window.location.assign('/userInfo');</script>")
        elif re.match(pattern, password):
            #비밀번호 암호화
            hlib = hashlib.sha256()
            hlib.update(password.encode("UTF-8"))
            password = hlib.hexdigest()
            user = Account.objects.get(email=email)
            if password == user.password:
                return render(request, "main/userInfo_modify.html", context={'user':user})
            else :
                return HttpResponse("<script>alert('비밀번호가 틀렸습니다.');window.location.assign('/userInfo');</script>")
        else :
            return HttpResponse("<script>alert('비밀번호는 영어 숫자만 사용하여 6자리부터 16자리까지만 가능합니다.');window.location.assign('/userInfo');</script>")
        
def modifyInfo(request):
    if request.method == "POST":
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
        user = Account.objects.get(email=email)
        user.email = email
        user.password = hlib.hexdigest()
        user.name = name
        user.gender = gender
        user.genre = genre
        user.save()
        request.session.flush()
        if not request.session.session_key:
            request.session.create()
        request.session["email"] = email
        request.session["userName"] = user.name
        return HttpResponse("<script>alert('수정이 완료되었습니다.');window.location.assign('/userInfo');</script>")

def deleteInfo(request):
    password = request.POST.get("pw_name")
    email = request.POST.get("email")
    pattern = r'^[a-zA-Z0-9]{6,16}$'
    if not request.session.session_key:
        return HttpResponse("<script>alert('세션이 만료되었습니다.');window.location.assign('/login');</script>")
    else :
        if password == '':
            return HttpResponse("<script>alert('비밀번호를 입력해주세요..');window.location.assign('/userInfo');</script>")
        elif re.match(pattern, password):
            #비밀번호 암호화
            hlib = hashlib.sha256()
            hlib.update(password.encode("UTF-8"))
            password = hlib.hexdigest()
            user = Account.objects.get(email=email)
            if password == user.password:
                return HttpResponse(
                    '<script>\
                        function realDelete() {\
                                if (!confirm("정말로 아이디를 지우시겠습니까?")) {\
                                    alert("아이디 삭제를 취소합니다.");\
                                    window.location.assign("/userInfo");\
                                } else {\
                                    alert("아이디를 삭제합니다.");\
                                    window.location.assign("/userInfo/delete/deleteid");\
                                }\
                            }\
                        realDelete();\
                    </script>'
                    )
            else :
                return HttpResponse("<script>alert('비밀번호가 틀렸습니다.');window.location.assign('/userInfo');</script>")
        else :
            return HttpResponse("<script>alert('비밀번호는 영어 숫자만 사용하여 6자리부터 16자리까지만 가능합니다.');window.location.assign('/userInfo');</script>")

def deleteID(request):
    user = Account.objects.get(email=request.session["email"])
    if request.method == "GET": 
        context = {
            "state" : 0,
            'user':user,
            }
        return render(request, "main/deleteID.html", context=context)
    
    # 삭제버튼을 누른경우
    elif request.method == "POST":
        context = None
        delete_ = request.POST.get("deleteID")

        if delete_ == '아이디삭제':
            user.delete()
            request.session.flush()
            context = {"state" : 1}
            return render(request, "main/deleteID.html", context=context)
        else :
            return HttpResponse("<script>alert('확인문구를 정확히 입력해주세요.');window.location.assign('/userInfo/delete/deleteid');</script>")

def saveHistory(user_id, query):
    # 연속 새로고침 에러 방지
    recent_history = SearchHistory.objects.filter(user_id=user_id).order_by('-id').first()
    if not recent_history == None:
        if recent_history.query == None:
            return
    if recent_history and recent_history.query == query:
        return
    search_history = SearchHistory(user_id=user_id, query=query)
    search_history.save()

        
def deleteRecord(request, id):
    user = Account.objects.get(email=request.session["email"])
    history_to_delete = SearchHistory.objects.filter(user_id=user, query=id)
    history_to_delete.delete()
    return redirect('main:userInfo')

def searchFunc(search,search_bar_category,offset):
    if search_bar_category == 'all':
        title = sp.search(q=f'{search}', type='track', offset={offset})
    elif search_bar_category == 'search_title':
        title = sp.search(q=f'title:{search}', type='track', offset={offset})
    elif search_bar_category == 'search_artist':
        title = sp.search(q=f'artist:{search}', type='track', offset={offset})
    return title
    
def search(request):
    if request.method == "GET":
        if not 'offset' in request.GET:
            return render(request, "main/search.html")
        else :
            try:
                offset = request.GET.get('offset', 'offset')
                search = request.GET.get('q', 'search')
                search_bar_category = request.GET.get('sc', 'search_bar_category')
                title = searchFunc(search,search_bar_category,offset)
                
                #raise 코드
                title['tracks']['items'][0]
                
                context = {
                    "spotipyDatas":title,
                    'search_bar_category':search_bar_category,
                    'search':search,
                    'offset':int(offset)
                    }
                return render(request, "main/search.html",context )
            except IndexError as ie:
                print(ie)
                context = {"state" : 0}
                return render(request, "main/search.html",context)
            except spoti.spotipy.exceptions.SpotifyException as se :
                print(se)
                return HttpResponse("<script>alert('검색 범위를 넘어갔습니다.');window.history.back();</script>")
    elif request.method == "POST":
        offset = request.GET.get('offset', 'offset')
        if not 'offset' in request.GET:
            offset = 0
        try:
            search_text = request.POST.get("search_text")
            search_select = request.POST.get('search_select')
            if not search_select in ['all', 'search_title', 'search_artist']:
                return HttpResponse("<script>alert('카테고리를 선택해주세요');window.location.assign('/');</script>")  

            else :
                title = None
                title = searchFunc(search_text,search_select,offset)
                # if search_select == 'all':
                #     title = sp.search(q=f'{search_text}', type='track', offset={offset})
                # elif search_select == 'search_title':
                #     title = sp.search(q=f'title:{search_text}', type='track', offset={offset})
                # elif search_select == 'search_artist':
                #     title = sp.search(q=f'artist:{search_text}', type='track', offset={offset})

                #raise 코드
                title['tracks']['items'][0]
                
                context = {
                    "spotipyDatas":title,
                    'search_bar_category':search_select,
                    'search':search_text,
                    'offset':int(offset)
                    }
                return render(request, "main/search.html", context)
        except IndexError as ie:
            print(ie)
            context = {"state" : 0}
            return render(request, "main/search.html",context)
        except spoti.spotipy.exceptions.SpotifyException as se :
            print(se)
            return HttpResponse("<script>alert('검색어를 입력해주세요');window.location.assign('/');</script>")
        

def introduce(request):
    introduceID = request.GET.get('id')
    if not introduceID:
        introduceID=0
    context = {
        'introduceID':int(introduceID)
    }
    return render(request, "main/introduce.html",context=context)


def result(request, id):
    # 노래 검색 기록 저장
    if request.session.session_key:
        user = Account.objects.get(email=request.session["email"])
        saveHistory(user, id)
    # 노래 검색
    track = sp.track(id)
    artist = sp.artist(track['artists'][0]['id'])

    service01 = s1.Service(id)
    service01.setMusicInfo(track, artist)

    service02 = s2.Service({"title":track['name'],"artist":track['artists'][0]['name']})

    service03 = s3.Service(id, track['preview_url'])
    recommendation = sp.recommendations(seed_tracks=[id],limit=20)
    if request.method == "GET":

        context = service01.getMusicInfo()
        context["state"] = 0
        context['recommendation'] = recommendation
        
        return render(request, "main/result.html", context=context)
    
    elif request.method == 'POST':
        # try :
            service_list = request.POST.getlist('service_list')
            # service 1 
            service02_result = {'data': {'comments': 0, 'likes': 0, 'views': 0}, 'error': True, 'result': '검사X'}
            context = service01.getMusicInfo()
            if '1' in service_list :
                post_data = {
                    "gender" : request.POST['gender'],
                    "re_inst" : request.POST['re_inst'],
                    "bass_type" : request.POST['bass_type'],
                    "rhythm" : request.POST['rhythm'],
                    "main_instr" : request.POST['main_instr'],
                    "english" : request.POST['english'],
                    "retro" : request.POST['retro'],
                    "lofi" : request.POST['lofi'],
                }

                audio_features = sp.audio_features(tracks=id)
                service01.createDataFrame(audio_features, post_data)
                service01_result = service01.runModel()
                context["service01_result"] = service01_result
            if '2' in service_list:
            # service 2
                service02_data = service02.getData()
                service02_result = service02.runModel(service02_data)
                
            if '3' in service_list:
                # service 3
                service3_df = service03.createDataFrame()
                service03_result = service03.runModel(service3_df)
                
                # print(len(service03_result)[0][0])
                if service03_result >= 0.5:
                    service03_result = '빌보드 올라갈 가능성이 높음'
                else :
                    service03_result = '빌보드 올라갈 가능성이 낮음'
                # import numpy as np
                context["service03_result"] = service03_result
                # print(np.where(service03_result > 0.5, 1, 0))
            
            context["service02_result"] = service02_result
            if service02_result == {'data': {'comments': 0, 'likes': 0, 'views': 0}, 'error': True, 'result': '가능성 없음'}:
                pass
            # # 모델 자동 추가 학습
            # if service_4 >= 0.5:
            #     y4data = np.array([1])
            # else :
            #     y4data = np.array([0])
            # model4.fit(X4data, y4data, epochs=10, verbose=2)
            # model4.save('main\static\models\service4\end_to_end_final32.h5')
            
            
            
            
            
            context["state"] = 1
            context['recommendation'] = recommendation
            return render(request, "main/result.html", context=context)
        # except TypeError as e:
        #     print(e)
        #     context = service01.getMusicInfo()
        #     context["service01_result"] = '스포티파이 정책에 의해 제한이 걸린 노래입니다..'
        #     context["state"] = 1

        #     return HttpResponse(f"spofty_limit:{id}")
        
def notfound(request):
    return render(request, "main/not_found.html")

