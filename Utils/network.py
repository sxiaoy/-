import json
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from Utils.tools import *
from DataBase.models import *
from datetime import datetime


def post_request(request):
    request = request.body.decode("utf-8")
    request = json.loads(request)
    return request


def new_record(mod, add):
    pass
    # BrowseRecord(TemporaryMotto=mod, browseRecord_partition=add).save()

# class TestingMiddlewareMixin(MiddlewareMixin):
#     def process_request(self, request):
#         # 第一个,视图之前
#
#         if request.method == "POST" and request.POST.get("token", ""):
#             try:
#                 token = request.POST.get("token")
#                 user = User.objects.filter(user_token=token)
#                 if user:
#                     user_id, time = des_decrypt(token, user.user_token_key)
#                     if user.id == user_id:
#                         pass
#
#             except:
#                 return fail(code=400, message="中间件except", data={})
#
#         print("222222")
#         return
#
#     def process_response(self, request, response):
#         # 返回的时候,视图之后
#         token, token_key = des_encryption(field=str(user.id) + "|||" + "sxiaoy")
#         user.user_token = token
#         user.user_token_key = token_key
#         response["data"]["token"] = token
#         return success(code=response["code"], message=response["message"], data=response["data"])
