# import asyncio
# import time
# import requests
#
# data = {
#     "_servicecode": "202104280948147173",
#     "_token": "dbc98d93b56f1eabd23d25769912115e",
#     "_orgid": "",
#     "_refuladdress": "api/statistic/totalStatistic"
# }
#
# header = {
#     "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3Nfa2V5IjoidVRjeWJrY0N2SU5zMXpRWFpKZ1M1TWhuODFHOWJ2a2UiLCJzZWNyZXRfa2V5IjoiWmhOSVF2bTgyRHJvMXlnbnRSS2lYRHFTa3FucjBHbHhjc3NFaGo0R0hHVVFOQ2NDNmhNY3owNWh2UlI2eXJNbiIsImV4cCI6MTYzOTcxNzYyMCwib3JpZ19pYXQiOjE2Mzk3MDk4MjB9.ILLixmjMo0-WVhezUWRGjk5WjfUZ96xiPabZYaPvUYw"
# }
#
#
# # 一个真实的耗时操作，可以比如去爬取网页
# def mysleep(x):
#     start_time = time.time()
#     value = requests.post(
#         url='http://10.20.111.68:8008/v1/api/data/10000001600?methodName=queryPaymentSharingPlatformAuthStatistics',
#         timeout=30, data=data, headers=header)
#     print(value.text)
#     print(time.time()-start_time)
#
#
# async def mytask(task_name):
#     print(task_name, 'start')
#     r = await asyncio.get_event_loop().run_in_executor(None, mysleep, 3)
#
#
# loop = asyncio.get_event_loop()
# tasks = []
# for i in range(500):
#     tasks.append(mytask('task{}'.format(i)))
# loop.run_until_complete(asyncio.wait(tasks))
# loop.close()

import json
import demjson
a = "[{'data_name': 'aaa', 'data_value': 'aaa', 'data_example': '', 'comments': ''}, {'data_name': 'bbb', 'data_value': 'bbb', 'data_example': '', 'comments': ''}]"
a = demjson.decode(a)
for i in a:
    print(i["data_name"])
    print(type(i))
# print(a)
# print(type(a))
