"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path 
from .views import *

urlpatterns = [
    path('' , index , name='index'),
    path('register/' , register , name='register'),
    path('login/' , login , name='login'),
    path('welcome/' , welcome , name='welcome'),
    path('post_job' , post_job , name='post_job'),
    path('course/' , course , name='course'),
 path('create-order/', create_order, name='create_order'),
]
