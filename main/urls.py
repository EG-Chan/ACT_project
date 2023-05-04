from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("search/", views.search, name="search"),
    path("userInfo/", views.userInfo, name="userInfo"),
]