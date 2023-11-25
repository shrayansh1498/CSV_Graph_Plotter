from django.contrib import admin
from django.urls import path
from CSV_Graph_Plotter import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.home, name='home2'),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
]