# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import json
import tornado.web
import tornado.gen
import tornado.ioloop

from wechatpy.client.async.tornado import AsyncWeChatClient


APPID = 'wxd7aa56e2c7b1f4f1'
SECRET = '2817b66a1d5829847196cf2f96ab2816'
OPENID = 'ozJS1syaqn5ztglMsr8ceH8o2zCQ'


class ExampleHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        client = AsyncWeChatClient(APPID, SECRET)
        try:
            user_info = yield client.user.get(OPENID)
        except Exception as e:
            print(e)
            self.write(str(e))
        else:
            self.set_header('Content-Type', 'text/plain')
            self.write(json.dumps(user_info))


if __name__ == '__main__':
    app = tornado.web.Application(
        handlers=[('/', ExampleHandler)],
        debug=True,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
