from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from websites import views
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('', login_required( views.Home.as_view() ), name="home"),
    path('register/', login_required( views.Register.as_view() ), name="websites-register"),
    path('remove/', login_required(views.remove), name="remove"),
    path('results/', login_required( views.Results.as_view() ), name="website-results"),
    path('check-script/', login_required( views.check_script ), name="check_script"),
    path('check-connections/', login_required( views.check_connections ), name="check_connections"),
    path('account-settings/', login_required( views.AccountSettings.as_view() ), name='account-settings'),
]
