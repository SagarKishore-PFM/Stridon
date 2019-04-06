from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='stridon_app/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),
    path('alice/', views.alice, name='alice'),
    path('doctor/', views.doctor, name='doctor'),
    path('subscribe/', views.subscribe, name='subscribe'),
]
