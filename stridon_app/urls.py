from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='stridon_app/login.html'
        ),
        name='login'
    ),
    path('signup/', views.signup, name='signup'),
    path('alice/', views.alice, name='alice'),
    path('doctor/', views.doctor, name='doctor'),
    path('subscribe/', views.subscribe, name='subscribe'),
    path('unsubscribe/', views.unsubscribe, name='unsubscribe'),
    path('add-article/', views.add_article, name='add-article'),
    re_path(
        r'^view_article/(?P<article_id>\d+)/$',
        views.view_article,
        name='view-article'
    ),
    path('articles-list/', views.list_articles, name='list-articles'),
]
