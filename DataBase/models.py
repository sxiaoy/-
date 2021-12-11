from django.db import models
from Utils.tools import *


class User(models.Model):
    """用户表"""
    user_username = models.CharField(max_length=20, default="用户{}".format(
        random_random(8, is_large=random_large, is_number=random_number, is_small=random_small)), null=True)  # 名称
    user_password = models.CharField(max_length=100)  # 密码
    user_creation_time = models.DateTimeField(auto_now_add=True)  # 账号创建时间

    class Meta:
        db_table = 'User'


class ShowUser(models.Model):
    """展示给用户的信息"""
    user_username = models.CharField(max_length=100)  # 展示用户名
    user_img = models.CharField(max_length=100)  # 图片
    user_email = models.CharField(max_length=100)  # 邮箱
    user_type = models.CharField(max_length=100)  # 状态
    user_motto = models.CharField(max_length=100)  # 座右铭.状态
    user_qq = models.CharField(max_length=100)  # qq

    class Meta:
        db_table = 'ShowUser'


class BrowseRecord(models.Model):
    """临时用户浏览记录"""
    TemporaryMotto = models.ForeignKey("TemporaryMotto", on_delete=models.SET_NULL, null=True)  # 临时浏览用户
    browseRecord_partition = models.CharField(max_length=30)  # 浏览文章id
    browseRecord_time = models.DateTimeField(auto_now_add=True)  # 浏览时间

    class Meta:
        db_table = 'BrowseRecord'


class TemporaryMotto(models.Model):
    """临时用户"""
    temporaryMotto_ip = models.CharField(max_length=200)  # ip地址
    temporaryMotto_name = models.CharField(max_length=200, default="")  # 名称
    temporaryMotto_time = models.DateTimeField(auto_now_add=True)  # 第一次浏览时间
    temporaryMotto_last = models.DateTimeField(auto_now=True)  # 最后一次浏览时间
    temporaryMotto_email = models.CharField(max_length=200, default="")  # 用户邮箱
    temporaryMotto_img = models.CharField(max_length=200, default="")  # 用户头像,如果邮箱为qq邮箱,通过qq邮箱获取

    class Meta:
        db_table = 'TemporaryMotto'


class Article(models.Model):
    """文章表"""
    article_title = models.CharField(max_length=255)  # 文章标题
    article_browse = models.CharField(max_length=255)  # 浏览数
    article_image = models.CharField(max_length=200)  # 图片url
    article_hits = models.IntegerField(default=0)  # 点赞数
    article_content = models.TextField()  # 文章内容
    article_time = models.DateTimeField(auto_now_add=True)  # 文章发布时间
    article_is_delete = models.IntegerField(default=0)  # 文章是否被删除

    class Meta:
        db_table = 'Article'


class Fabulous(models.Model):
    """点赞表"""
    Article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True)  # 文章
    TemporaryMotto = models.ForeignKey("TemporaryMotto", on_delete=models.SET_NULL, null=True)  # 点赞人
    comment_time = models.DateTimeField(auto_now_add=True)  # 点赞时间

    class Meta:
        db_table = 'Fabulous'


class Comment(models.Model):
    """文章评论"""
    Article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True)  # 文章
    comment_content = models.TextField()  # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    TemporaryMotto = models.ForeignKey("TemporaryMotto", on_delete=models.SET_NULL, null=True)  # 评论人

    class Meta:
        db_table = 'Comment'


class CommentSecondary(models.Model):
    """二级评论"""
    Article = models.ForeignKey("Article", on_delete=models.SET_NULL, null=True)  # 文章
    Comment = models.ForeignKey("Comment", on_delete=models.SET_NULL, null=True)  # 文章评论
    comment_content = models.TextField()  # 评论内容
    comment_time = models.DateTimeField(auto_now_add=True)  # 评论时间
    TemporaryMotto = models.ForeignKey("TemporaryMotto", on_delete=models.SET_NULL, null=True)  # 评论人

    class Meta:
        db_table = 'CommentSecondary'


class Music(models.Model):
    """音乐"""
    music_img = models.CharField(max_length=200)  # 歌曲img
    music_url = models.CharField(max_length=200)  # 歌曲mp3地址
    music_name = models.CharField(max_length=200)  # 歌曲名称
    music_type = models.IntegerField(default=0)  # 歌曲是否展示

    class Meta:
        db_table = 'Music'


class Image(models.Model):
    """图片"""
    image_add = models.CharField(max_length=200)  # 图片地址
    image_type = models.CharField(max_length=200)  # 图片类型
    image_time = models.DateTimeField(auto_now_add=True)  # 添加时间

    class Meta:
        db_table = 'Image'


class Book(models.Model):
    """书城"""
    book_name = models.CharField(max_length=200)  # 书名
    book_image = models.CharField(max_length=200)  # 封面
    book_author = models.CharField(max_length=200)  # 作者
    book_type = models.CharField(max_length=200)  # 小说类型
    book_brief = models.TextField()  # 简介
    book_is_end = models.CharField(max_length=200)  # 是否完结
    book_newest_time = models.CharField(max_length=200)  # 更新时间
    book_newest = models.CharField(max_length=200)  # 最新章节
    book_is_show = models.IntegerField(default=0)  # 是否展示
    book_url = models.CharField(max_length=200)  # 小说url

    class Meta:
        db_table = 'Book'


class Friend(models.Model):
    """朋友们"""
    friend_name = models.CharField(max_length=200)  # 网站名称
    friend_url = models.CharField(max_length=200)  # 网站url
    friend_img = models.CharField(max_length=200)  # 网站img
    friend_introduce = models.CharField(max_length=200)  # 网站介绍
    friend_time = models.DateTimeField(auto_now_add=True)  # 添加时间
    friend_is_show = models.IntegerField(default=0)  # 是否展示
    friend_invalid = models.IntegerField(default=0)  # 是否失效

    class Meta:
        db_table = 'Friend'


