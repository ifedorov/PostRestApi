"""PostBot URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, re_path

from StarNaviApp import views

# Create a router and register our viewsets with it.


urlpatterns = [

    path(r'v1/post', views.PostViewSet.as_view({'get': 'list', 'post': 'create'})),
    re_path(r'^v1/post/(?P<pk>([0-9a-zA-Z])+)/like$', views.PostViewSet.as_view({'put': 'like'})),
    re_path(r'^v1/post/(?P<pk>([0-9a-zA-Z])+)/unlike$', views.PostViewSet.as_view({'put': 'unlike'})),

    path(r'v1/user/token', views.UserCreateViewSet.as_view({'post': 'token'})),
    path(r'v1/user/sing-up', views.UserCreateViewSet.as_view({'post': 'sing_up'})),

    path('admin/', admin.site.urls),
]
