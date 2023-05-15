from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("signup/", views.signup, name="signup"),
    path("search/", views.search, name="search"),
    
    path("result/<str:id>", views.result, name="result"),
    path("userInfo/", views.userInfo, name="userInfo"),
    path("userInfo/change", views.changeInfo, name="changeInfo"),
    path("userInfo/change/modify", views.modifyInfo, name="modifyInfo"),
    path("userInfo/delete", views.deleteInfo, name="deleteInfo"),
    path("userInfo/delete_record/<str:id>", views.deleteRecord, name="deleteRecord"),
    path("userInfo/delete/deleteid", views.deleteID, name="deleteID"),
    path("introduce/", views.introduce, name="introduce"),

    path("notfound/", views.notfound, name="404notfound"),
    path("invalidRequest/", views.invalidRequest, name="invalidRequest"),
]