from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse

#사용자 정보 저장
from datetime import datetime
import hashlib

#모델
from main.models import Account


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
                request.session["email"] = email
                request.session["userName"] = user.name
                context = {
                    "sessionID" : request.session.session_key,
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

            context = {"state" : 1}
        except:
            context = {"state" : 2}
        finally:
            return render(request, "main/signup.html", context=context)
        

def userInfo(request):
    context = {
        "email": request.session["email"]
    }
    return render(request, "main/userInfo.html", context=context)


def search(request):

    if request.method == "GET":
        return render(request, "main/search.html")

    elif request.method == "POST":
        try:
            search = request.POST.get("search")
            search_bar_category = request.POST.get('search_bar')
            if search_bar_category == 'all':
                title = sp.search(q=f'{search}', type='track')
            elif search_bar_category == 'search_title':
                title = sp.search(q=f'title:{search}', type='track')
            elif search_bar_category == 'search_artist':
                title = sp.search(q=f'artist:{search}', type='track')
            else :
                return HttpResponse("<script>alert('카테고리를 선택해주세요');window.location.assign('/');</script>")
            return render(request, "main/search.html", {"spotipyDatas":title,'search_bar_category':search_bar_category,'search':search})
        except spoti.spotipy.exceptions.SpotifyException as se :
            print(se)
            return HttpResponse("<script>alert('검색어를 입력해주세요');window.location.assign('/');</script>")
            
        

        

        


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
        
def notfound(request):
    return render(request, "main/not_found.html")

