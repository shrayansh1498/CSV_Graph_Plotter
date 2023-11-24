from django.contrib import admin
from django.urls import path
from CSV_Graph_Plotter import views

urlpatterns = [
    path('', views.index, name='home'),
    path('home', views.index, name='home'),
    path('about', views.about, name='about'),
    path('services', views.services, name='services'),
    path('contact', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.logout_user, name='logout'),
]