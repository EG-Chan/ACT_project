from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
    path('login/',
        auth_views.LoginView.as_view(),
        name='login'
    ),

    path('logout/',
    auth_views.LoginView.as_view(),
    name='logout'
    ),

    path('signup/', views.signup, name='signup'),
]