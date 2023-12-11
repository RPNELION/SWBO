"""
URL configuration for SWBO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('signout/', signout, name='signout'),
    path('upload-avatar/', upload_avatar, name='upload_avatar'),
    path('change-password/', change_password, name='change_password'),
    path('delete-account/', delete_account, name='delete_account'),
    path('', homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('homepage/', homepage, name='homepage_url'),
    path('zadanie/', zadanie, name='zadanie'),
    path('zadaniaD/', zadania_dodaj, name='zadania_dodaj'),
    path('zadaniaU/', zadania_usun, name='zadania_usun'),
    path('zadaniaW/', zadania_wyszukaj, name='zadania_wyszukaj'),
    path('baza/', baza, name='baza'),
]
