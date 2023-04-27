from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'main'

urlpatterns = [
  path('login/', auth_views.LoginView.as_view(template_name='main/login.html'), name='login'),
  path('logout/', auth_views.LoginView.as_view(template_name='main/logout.html'), name='logout'),
  path('signup/', views.signup),
]