from DataBase.models import *
from Utils.tools import *
from Utils.network import *
import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import requests
from lxml import etree


def get_book(request):
    """
    根据条件返回书籍列表
    :param request:
    :return:
    """
    request = post_request(request)
    page_size = int(request['page']) * 10
    if request['type'] == 'all' and request['isEnd'] == 'all':
        book = Book.objects.filter()[page_size:10 + page_size]
    elif request['type'] == 'all':
        book = Book.objects.filter(book_is_end=request['isEnd'])[page_size:10 + page_size]
    elif request['isEnd'] == 'all':
        book = Book.objects.filter(book_type=request['type'])[page_size:10 + page_size]
    else:
        book = Book.objects.filter(book_is_end=request['isEnd'], book_type=request['type'])[page_size:10 + page_size]
    book = queryset(book)
    return success(data=book)


def get_book_len(request):
    book = Book.objects.all().count()
    return success(data=book)


def get_book_see(request):
    request = post_request(request)
    get_info = requests.get(url=request['url'], headers={'User-Agent': random_header()}, timeout=10)
    get_info = etree.HTML(get_info.content)
    chapter = get_info.xpath("//div[@class='mulu']//li/a/text()")
    chapter_url_list = get_info.xpath("//div[@class='mulu']//li/a/@href")
    chapter_url = []
    for i in chapter_url_list:
        chapter_url.append('http://www.88xdushu.com' + i)
    return success(data={'chapter': chapter, 'chapter_url': chapter_url})


def book_content(request):
    request = post_request(request)
    get_info = requests.get(url=request['url'], headers={'User-Agent': random_header()}, timeout=10)
    get_info = etree.HTML(get_info.content)
    content = get_info.xpath("//div[@class='yd_text2']//text()")
    content = content[0:len(content) - 9]
    return success(data=content)


def update_book_url(request):
    book = Book.objects.filter()
    for i in book:
        update_book = Book.objects.filter(pk=i.id).update(book_image=i.book_image.replace('88xdushu', 'zzhtc'),)
    return success()
