from django.contrib import admin
from django.urls import path
from select_hobby import views

urlpatterns = [
    path('recommend/', views.recommend, name='recommend'),
    path('create/', views.create, name='create'),
] 
