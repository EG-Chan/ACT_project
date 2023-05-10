from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("search/", views.search, name="search"),
<<<<<<< HEAD
    path("result/", views.result, name="result"),
=======
    path("result/<str:id>", views.result, name="result"),
>>>>>>> c7edc1144d03729a39f638bd708af46496d1e4d4
    path("userInfo/", views.userInfo, name="userInfo"),
    path("introduce/", views.introduce, name="introduce"),
]