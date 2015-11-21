# -*- coding: utf-8 -*-
import json
import asyncio
from aiohttp.web import Application, Response

from wechatpy.client.async.asyncio import AsyncWeChatClient


APPID = 'wxd7aa56e2c7b1f4f1'
SECRET = '2817b66a1d5829847196cf2f96ab2816'
OPENID = 'ozJS1syaqn5ztglMsr8ceH8o2zCQ'


@asyncio.coroutine
def user_info(request):
    resp = Response()
    client = AsyncWeChatClient(APPID, SECRET)
    try:
        user = yield from client.user.get(OPENID)
    except Exception as e:
        print(e)
        resp.body = str(e).encode('utf-8')
    else:
        resp.body = json.dumps(user).encode('utf-8')
    return resp


@asyncio.coroutine
def user_group_id(request):
    resp = Response()
    client = AsyncWeChatClient(APPID, SECRET)
    try:
        group_id = yield from client.user.get_group_id(OPENID)
    except Exception as e:
        print(e)
        resp.body = str(e).encode('utf-8')
    else:
        resp.body = str(group_id).encode('utf-8')
    return resp


@asyncio.coroutine
def main(loop):
    app = Application(loop=loop)
    app.router.add_route('GET', '/', user_info)
    app.router.add_route('GET', '/group_id', user_group_id)

    handler = app.make_handler()
    srv = yield from loop.create_server(handler, '127.0.0.1', 8888)
    print("Server started at http://127.0.0.1:8888")
    return srv, handler


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    srv, handler = loop.run_until_complete(main(loop))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        loop.run_until_complete(handler.finish_connections())
