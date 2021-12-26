from django.http import JsonResponse
import random
from datetime import datetime
import json
from django.forms.models import model_to_dict
import time
import base64
import platform
from PIL import Image
import os

header_list = [
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
    'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11',
    'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPod; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (iPad; U; CPU OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
    'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; Nexus One Build/FRF91) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Opera/9.80 (Android 2.3.4; Linux; Opera Mobi/build-1107180945; U; en-GB) Presto/2.8.149 Version/11.10'
]
random_large = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
                "S", "T", "U", "V", "W", "X", "Y", "Z"]
random_small = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r",
                "s", "t", "u", "v", "w", "x", "y", "z"]
random_number = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]


def random_random(length, is_large=[], is_small=[], is_number=[]):
    random_list = is_large + is_small + is_number
    random_str = "".join(random.sample(random_list, length))
    return random_str


def add_address():
    if is_system():
        return "http://127.0.0.1:8000"
    else:
        return "https://www.sxiaoy.cn"


class HttpCode(object):
    success = 200
    fail = 400
    parameter_error = 1000
    no_registration = 1001


def result(code=HttpCode.success, message="", data=None, kwarge=None):
    json_dict = {"code": code, "message": message, "data": data}
    if kwarge and isinstance(kwarge, dict) and kwarge.keys():
        json_dict.update(kwarge)
    return JsonResponse(json_dict)


def random_header():
    return "".join(random.sample(header_list, 1))


def success(code=HttpCode.success, message="", data=None, kwarge=None):
    return result(code=code, message=message, data=data)


def fail(code=HttpCode.fail, message="", data=None, kwarge=None):
    return result(code=code, message=message, data=data)


def time_str(datetime_str):
    return str(datetime_str).split('.')[0].replace('T', ' ').split('+')[0]


def random_img():
    img_list = ['https://p.qqan.com/up/2021-10/16332291748091917.jpg',
                'https://p.qqan.com/up/2021-10/16332291752641599.jpg']
    return random.choice(img_list)


def default(obj_dict):
    import json
    from django.core import serializers
    json_data = serializers.serialize('json', obj_dict)
    json_data = json.loads(json_data)
    from django.http import HttpResponse, JsonResponse
    return JsonResponse(json_data, safe=False)


def queryset(obj):
    obj_list = []
    for i in obj:
        obj_list.append(model_to_dict(i))
    return obj_list


def date_interval(date_str):
    '''
    获取时间间隔
    1分钟前，2分钟前，10分钟前，1小时前，2小时前，1天前，2天前，3天前，1个月前，3个月前，1年前，3年前
    :param date_str: 时间字符串
    :return: 字符串
    '''
    date_str = time.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    # 将时间元组转换为时间戳
    t = time.mktime(date_str)

    # 当前时间
    seconds = time.time() - t

    years = int(seconds // (60 * 60 * 24 * 365))
    if years:
        return '{}年前'.format(years)
    months = int(seconds // (60 * 60 * 24 * 30))
    if months:
        return '{}月前'.format(months)
    days = int(seconds // (60 * 60 * 24))
    if days:
        return '{}天前'.format(days)
    hours = int(seconds // (60 * 60))
    if hours:
        return '{}小时前'.format(hours)
    minutes = int(seconds // (60))
    if minutes:
        return '{}分钟前'.format(minutes)
    return '刚刚'


def safe_base64_decode(s):
    # 判断是否是4的整数u，不够的在末尾添加等号
    if len(s) % 4 != 0:
        s = s + bytes('=', encoding='utf-8') * (4 - len(s) % 4)
    # 解决字符串和bytes类型
    if not isinstance(s, bytes):
        s = bytes(s, encoding='utf-8')
    # 解码
    base64_str = base64.b64decode(s)

    return base64_str


def get_size(filename):
    size = os.path.getsize(filename)
    return size / 1024


def compress_image(img_path, out_path, quality, mb=500, step=5):
    """不改变图片尺寸压缩图像大小
    :param img_path: 压缩图像读取地址
    :param out_path: 压缩图像存储地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    # o_size = get_size(img_path)
    # if o_size < mb:
    #     return Image.open(img_path)
    # img = Image.open(img_path)
    # while o_size > mb:
    img = Image.open(img_path)
    img = img.convert('RGB')
    img.save(out_path, quality=quality)
    # if quality - step < 0:
    #     break
    # quality -= step
    return img


def is_system():
    if platform.system().lower() == 'windows':
        return True
    elif platform.system().lower() == 'linux':
        return False
