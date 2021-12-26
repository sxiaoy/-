import time

from DataBase.models import *
from Utils.tools import *
from Utils.network import *
import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models import F
import os
import base64


def personal_info(request):
    """
    返回个人信息
    :param request:
    :return ShowUser:
    """
    request = post_request(request)
    temporary = TemporaryMotto.objects.filter(temporaryMotto_ip=request["ip"]).first()
    if temporary:
        # new_record(temporary, request["add"])
        return success(data=model_to_dict(ShowUser.objects.first()))
    TemporaryMotto(temporaryMotto_ip=request["ip"]).save()
    # new_record(TemporaryMotto.objects.filter(temporaryMotto_ip=request["ip"]).first(), request["add"])
    return success(data=model_to_dict(ShowUser.objects.first()))


def update_personal(request):
    """
    修改个人信息
    :param request:
    :return:
    """
    request = post_request(request)
    user = request['user']
    ShowUser.objects.filter(pk=user['id']).update(user_username=user['user_username'],
                                                  user_img=user['user_img'],
                                                  user_email=user['user_email'],
                                                  user_type=user['user_type'],
                                                  user_motto=user['user_motto'],
                                                  user_qq=user['user_qq'])
    return success()


def article_list(request):
    """
    返回文章列表
    :param request:
    :return list[0:10]:
    """
    request = post_request(request)
    article_queryset = Article.objects.filter(article_is_delete=0).order_by('-article_time')
    article = queryset(article_queryset)
    for i in range(len(article)):
        article[i]["article_time"] = date_interval(article_queryset[i].article_time.strftime('%Y-%m-%d %H:%M:%S'))
        article[i]["specific"] = time_str(article_queryset[i].article_time)
    return success(data={
        'article_length': len(article),
        'article': article[int(request["page"]) - 10:int(request["page"])]
    })


def get_id_article(request):
    """
    根据id返回文章
    :param request:
    :return:
    """
    request = post_request(request)
    article_models = Article.objects.filter(article_is_delete=0, pk=request['id']).first()
    article = model_to_dict(article_models)
    article['article_time'] = time_str(article_models.article_time)
    return success(data=article)


def about_me(request):
    """
    返回关于我文章
    :param request:
    :return json:
    """
    article_queryset = Article.objects.filter(article_is_delete=2).first()
    article = model_to_dict(article_queryset)
    article["article_time"] = date_interval(article_queryset.article_time.strftime('%Y-%m-%d %H:%M:%S'))
    return success(data=article)


def get_music(request):
    """
    返回音乐列表
    :param request:
    :return list:
    """
    return success(data=queryset(Music.objects.all()))


def update_article(request):
    """
    修改文章内容
    :param request:
    :return:
    """
    request = post_request(request)
    article = request['article']
    Article.objects.filter(pk=article['id']).update(article_title=article['article_title'],
                                                    article_image=article['article_image'],
                                                    article_hits=article['article_hits'],
                                                    article_browse=article['article_browse'],
                                                    article_is_delete=article['article_is_delete'],
                                                    article_content=article['article_content'])

    return success()


def insert_article(request):
    """
    添加文章
    :param request:
    :return:
    """
    request = post_request(request)
    article = request['article']
    Article(article_title=article['article_title'], article_image=article['article_image'],
            article_hits=article['article_hits'], article_browse=article['article_browse'],
            article_is_delete=article['article_is_delete'], article_content=article['article_content']).save()

    return success()


def comment_info(request):
    """
    获取文章评论
    :param id:
    :return list:
    """
    request = post_request(request)
    comment = Comment.objects.filter(Article=request['id']).order_by('-comment_time')
    comment_list = []
    for i in range(len(comment)):
        comment_list.append(model_to_dict(comment[i]))
        comment_list[i]['comment_time'] = time_str(comment[i].comment_time)
        comment_secondary = CommentSecondary.objects.filter(Article=request['id'], Comment=comment[i].id).order_by(
            '-comment_time')
        temporary_motto = model_to_dict(TemporaryMotto.objects.filter(pk=comment[i].TemporaryMotto_id).first())
        comment_list[i]['temporary_id'] = temporary_motto['id']
        comment_list[i]['temporaryMotto_name'] = temporary_motto['temporaryMotto_name']
        comment_list[i]['temporaryMotto_img'] = temporary_motto['temporaryMotto_img']
        comment_secondary_list = []
        for j in range(len(comment_secondary)):
            comment_secondary_list.append(model_to_dict(comment_secondary[j]))
            comment_secondary_list[j]['comment_time'] = time_str(comment_secondary[j].comment_time)
            temporary_motto2 = model_to_dict(
                TemporaryMotto.objects.filter(pk=comment_secondary[j].TemporaryMotto_id).first())
            comment_secondary_list[j]['temporary_id'] = temporary_motto2['id']
            comment_secondary_list[j]['temporaryMotto_name'] = temporary_motto2['temporaryMotto_name']
            comment_secondary_list[j]['temporaryMotto_img'] = temporary_motto2['temporaryMotto_img']
        comment_list[i]['comment_secondary'] = comment_secondary_list
    return success(data=comment_list)


def new_comment(request):
    """
    添加评论或者子评论
    :param request:
    :return:
    """
    request = post_request(request)
    temporary_motto = TemporaryMotto.objects.filter(temporaryMotto_email=request['commentEmail']).first()
    if not temporary_motto:
        temporary_motto_img = random_img()
        if '@qq.com' in request['commentEmail']:
            temporary_motto_img = 'https://q1.qlogo.cn/g?b=qq&nk={}&s=100'.format(
                str(request['commentEmail']).split('@')[0])
        TemporaryMotto.objects.filter(temporaryMotto_ip=request['temporaryMottoIp']).update(
            temporaryMotto_name=request['commentName'], temporaryMotto_email=request['commentEmail'],
            temporaryMotto_img=temporary_motto_img)
        temporary_motto = TemporaryMotto.objects.filter(temporaryMotto_email=request['commentEmail']).first()
    temporary_motto = model_to_dict(temporary_motto)
    comment_dict = {}
    comment_dict['temporary_id'] = temporary_motto['id']
    comment_dict['temporaryMotto_name'] = temporary_motto['temporaryMotto_name']
    comment_dict['temporaryMotto_img'] = temporary_motto['temporaryMotto_img']
    if int(request['type']) == 1:
        commit = Comment(Article_id=request['articleId'], comment_content=request['commentContent'],
                         TemporaryMotto_id=int(temporary_motto['id']))
        commit.save()
        commit_list = model_to_dict(commit)
        commit_list['comment_time'] = time_str(commit.comment_time)
        commit_list = dict(commit_list, **comment_dict)
        return success(data=commit_list)
    else:
        comment_secondary = CommentSecondary(Article_id=request['articleId'], comment_content=request['commentContent'],
                                             Comment_id=request['temporaryId'],
                                             TemporaryMotto_id=int(temporary_motto['id']))
        comment_secondary.save()
        comment_secondary_list = model_to_dict(comment_secondary)
        comment_secondary_list['comment_time'] = time_str(comment_secondary.comment_time)
        comment_secondary_list = dict(comment_secondary_list, **comment_dict)
        return success(data=comment_secondary_list)


def add_hits(request):
    """
    文章点赞
    :param request:
    :return:
    """
    request = post_request(request)
    temporary_motto = TemporaryMotto.objects.filter(temporaryMotto_ip=request['temporaryId']).first()
    fabulous = Fabulous.objects.filter(Article=request['articleId'], TemporaryMotto=temporary_motto.id).first()
    if fabulous:
        return success(message='已经点过赞了')
    Fabulous(Article_id=request['articleId'], TemporaryMotto_id=temporary_motto.id).save()
    Article.objects.filter(pk=request['articleId']).update(article_hits=F('article_hits') + 1)
    return success(message='谢谢你的鼓励')


def get_img(request):
    """
    返回图片列表
    :param request:
    :return:
    """
    request = post_request(request)
    img_type = request['type']
    img_type = img_type if img_type != "free" else "1"
    print(img_type)
    if img_type == 'all':
        img_list = Image.objects.filter().order_by('-image_time')
    else:
        img_list = Image.objects.filter(image_type=img_type).order_by('-image_time')
    img = queryset(img_list)
    for i in range(len(img)):
        img[i]["image_time"] = time_str(img_list[i].image_time)
    return success(data=img)


def load_img(request):
    """
    上传图片
    :param request:
    :return:
    """
    request = post_request(request)
    picture = safe_base64_decode(str(request['formData']).split(",")[1])
    img_name = random_random(8, random_large, random_small, random_number)
    file = open('static/image/{}.jpg'.format(img_name), 'wb')
    file.write(picture)
    file.close()
    compress_image('static/image/{}.jpg'.format(img_name), 'static/image/{}.jpg'.format(img_name), 90)
    img_add = add_address() + '/static/image/{}.jpg'.format(img_name)
    image = Image(image_type=int(request['type']), image_add=img_add)
    image.save()
    img = model_to_dict(image)
    img['image_time'] = image.image_time
    return success(data=img)


def update_img(request):
    """
    修改图片类型
    :param request:
    :return:
    """
    request = post_request(request)
    Image.objects.filter(pk=request['id']).update(image_type=request['type'])
    return success()


def delete_img(request):
    """
    删除图片
    :param request:
    :return:
    """
    request = post_request(request)
    Image.objects.filter(pk=request['id']).delete()
    return success()


def get_friend(request):
    """
    获取我的朋友们
    :param request:
    :return:
    """
    request = post_request(request)
    if request['type'] == 'all':
        friend_contact = queryset(
            Friend.objects.filter(friend_is_show=0).all().order_by('-friend_time'))
        return success(data=friend_contact)
    friend_contact_on = queryset(
        Friend.objects.filter(friend_is_show=0, friend_invalid=0).all().order_by('-friend_time'))
    friend_contact_off = queryset(
        Friend.objects.filter(friend_is_show=0, friend_invalid=1).all().order_by('-friend_time'))
    friend_small = queryset(
        Friend.objects.filter(friend_is_show=0, friend_invalid=2).all().order_by('-friend_time'))
    return success(data=[friend_contact_on, friend_contact_off, friend_small])


def add_friend(request):
    """
    添加一个朋友
    :param request:
    :return:
    """
    request = post_request(request)
    friend = request['friend']
    f = Friend(friend_name=friend['friend_name'], friend_url=friend['friend_url'], friend_img=friend['friend_img'],
               friend_introduce=friend['friend_introduce'], friend_is_show=friend['friend_is_show'],
               friend_invalid=friend['friend_invalid'])
    f.save()
    friend = model_to_dict(f)
    return success(data=friend)


def update_friend(request):
    """
    修改一个朋友信息
    :param request:
    :return:
    """
    request = post_request(request)
    friend = request['friend']
    Friend.objects.filter(pk=friend['id']). \
        update(friend_name=friend['friend_name'], friend_url=friend['friend_url'], friend_img=friend['friend_img'],
               friend_introduce=friend['friend_introduce'], friend_is_show=friend['friend_is_show'],
               friend_invalid=friend['friend_invalid'])
    return success()


def zip_img(request):
    """
    压缩图片
    :param request:
    :return:
    """
    request = post_request(request)
    picture = safe_base64_decode(str(request['formData']).split(",")[1])
    img_path = random_random(8, random_large, random_small, random_number)
    out_path = random_random(8, random_large, random_small, random_number)
    file = open('static/temporary/{}.jpg'.format(img_path), 'wb')
    file.write(picture)
    file.close()
    quality = 100 - int(request['quality'])
    compress_image('static/temporary/{}.jpg'.format(img_path), 'static/temporary/{}.jpg'.format(out_path), quality)
    with open('static/temporary/{}.jpg'.format(out_path), 'rb') as f:
        image = f.read()
    img_base64 = str(base64.b64encode(image), encoding='utf-8')
    return success(data={
        'img_url': add_address() + '/static/temporary/{}.jpg'.format(img_path),
        'img_base64': img_base64
    })
