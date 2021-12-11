from django.conf.urls import url
from .views import *
from django.urls import path
urlpatterns = [
    path("login/", login),
    path("test/", test),
    path("initialization/", initialization),
]
