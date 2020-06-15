"""koimetrics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from koimetrics import settings
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from profiles.views import SignUp, Login
from django.contrib.auth.views import LogoutView
from django.http import HttpResponse

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda r : render(r,"web/index.html"), name="index"),
    path('dashboard/', include("websites.urls")),
    path('signup/', SignUp.as_view(), name="signup"),
    path('login/', Login.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
