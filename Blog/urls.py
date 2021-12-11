from django.conf.urls import url
from .views import *
from django.urls import path

urlpatterns = [
    path("personal_info/", personal_info),
    path("article_list/", article_list),
    path("get_music/", get_music),
    path("update_article/", update_article),
    path("insert_article/", insert_article),
    path("comment_info/", comment_info),
    path("new_comment/", new_comment),
    path("add_hits/", add_hits),
    path("about_me/", about_me),
    path("load_img/", load_img),
    path("get_img/", get_img),
    path("delete_img/", delete_img),
    path("update_img/", update_img),
    path("get_id_article/", get_id_article),
    path("get_friend/", get_friend),
    path("add_friend/", add_friend),
    path("update_friend/", update_friend),
    path("update_personal/", update_personal),
    path("zip_img/", zip_img),

]
