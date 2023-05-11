from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator

#사용자 정보 저장
from datetime import datetime
import hashlib

#모델
from main.models import Account

# 
import re

#사용자 모듈 불러오기
from main.moduleFolder import service01 as s1
from main.moduleFolder import service02 as s2
from main.moduleFolder import service03 as s3
from main.moduleFolder import spoti

sp = spoti.Spoti().getSpotiData()

def main(request):
    return render(request, "main/main.html")


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
        

def userInfo(request):
    try:
        if not request.session.session_key:
            return HttpResponse("<script>alert('세션이 만료되었습니다.');window.location.assign('/login');</script>")
        elif request.session.session_key:
            user = Account.objects.get(email=request.session["email"])
            context = {
                'user':user,
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
            search = request.POST.get("search")
            search_bar_category = request.POST.get('search_bar')
            if not search_bar_category in ['all', 'search_title', 'search_artist']:
                return HttpResponse("<script>alert('카테고리를 선택해주세요');window.location.assign('/');</script>")  

            else :
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
            return HttpResponse("<script>alert('검색어를 입력해주세요');window.location.assign('/');</script>")

def searchFunc(search,search_bar_category,offset):
    if search_bar_category == 'all':
        title = sp.search(q=f'{search}', type='track', offset={offset})
    elif search_bar_category == 'search_title':
        title = sp.search(q=f'title:{search}', type='track', offset={offset})
    elif search_bar_category == 'search_artist':
        title = sp.search(q=f'artist:{search}', type='track', offset={offset})
    return title

        
def introduce(request):
    return render(request, "main/introduce.html")


def result(request, id):
    
    # 노래 검색
    track = sp.track(id)
    artist = sp.artist(track['artists'][0]['id'])

    service01 = s1.Service(id)
    service01.setMusicInfo(track, artist)

    service03 = s3.Service(id, track['preview_url'])
    recommendation = sp.recommendations(seed_tracks=[id],limit=5)
    if request.method == "GET":

        context = service01.getMusicInfo()
        context["state"] = 0
        context['recommendation'] = recommendation
        
        return render(request, "main/result.html", context=context)
    
    elif request.method == 'POST':
        try :
            # service_1 
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

            # service 3
            service03.createDataFrame()
            service03_result = service03.runModel()
            
            # # 모델 자동 추가 학습
            # if service_4 >= 0.5:
            #     y4data = np.array([1])
            # else :
            #     y4data = np.array([0])
            # model4.fit(X4data, y4data, epochs=10, verbose=2)
            # model4.save('main\static\models\service4\end_to_end_final32.h5')
            
            context = service01.getMusicInfo()
            context["service01_result"] = service01_result
            context["service03_result"] = service03_result
            context["state"] = 1
            context['recommendation'] = recommendation
            
            return render(request, "main/result.html", context=context)
        except TypeError as e:
            print(e)
            context = service01.getMusicInfo()
            context["service01_result"] = '해당국가에서는 검색이 안되는 노래입니다.'
            context["state"] = 1

            return HttpResponse(f"<script>alert('해당국가에서는 검색이 안되는 노래입니다.');window.location.assign('/result/{id}');</script>")
        

