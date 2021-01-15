# -*- coding: utf-8 -*-
import time

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from wechatpy import WeChatClient


def index(request):
    return render(request, "index.html")


@csrf_exempt
def jsapi_signature(request):
    noncestr = "123456"
    timestamp = int(time.time())
    url = request.POST["url"]

    client = WeChatClient(settings.WECHAT_APPID, settings.WECHAT_SECRET)
    ticket_response = client.jsapi.get_ticket()
    signature = client.jsapi.get_jsapi_signature(noncestr, ticket_response["ticket"], timestamp, url)
    ret_dict = {
        "noncestr": noncestr,
        "timestamp": timestamp,
        "url": url,
        "signature": signature,
    }
    return JsonResponse(ret_dict)


def log(request):
    print("Hello World!")
    return JsonResponse(
        {
            "status": "ok",
        }
    )
