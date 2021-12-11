from django.conf.urls import url
from .views import *
from django.urls import path


urlpatterns = [
    path("get_book/", get_book),
    path("get_book_len/", get_book_len),
    path("get_book_see/", get_book_see),
    path("update_book_url/", update_book_url),
    path("book_content/", book_content),

]
