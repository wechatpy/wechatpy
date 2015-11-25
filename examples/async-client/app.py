# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
import os
import json
import tornado.web
import tornado.gen
import tornado.ioloop

from wechatpy.client.async.tornado import AsyncWeChatClient


APPID = 'wxd7aa56e2c7b1f4f1'
SECRET = '2817b66a1d5829847196cf2f96ab2816'
OPENID = 'ozJS1syaqn5ztglMsr8ceH8o2zCQ'


class UserInfoHandler(tornado.web.RequestHandler):

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


class UserGroupHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        client = AsyncWeChatClient(APPID, SECRET)
        try:
            group_id = yield client.user.get_group_id(OPENID)
        except Exception as e:
            print(e)
            self.write(str(e))
        else:
            self.write(str(group_id))


class MediaUploadHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        img_path = os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            'doge.jpeg'
        )
        client = AsyncWeChatClient(APPID, SECRET)
        try:
            with open(img_path) as media_file:
                res = yield client.media.upload('image', media_file)
        except Exception as e:
            print(e)
            self.write(str(e))
        else:
            self.write(json.dumps(res))


class MenuUpdateHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        menu_data = {
            'button': [
                {
                    'type': 'click',
                    'name': 'test',
                    'key': 'test'
                }
            ]
        }
        client = AsyncWeChatClient(APPID, SECRET)
        try:
            res = yield client.menu.create(menu_data)
        except Exception as e:
            print(e)
            self.write(str(e))
        else:
            self.write(json.dumps(res))


if __name__ == '__main__':
    app = tornado.web.Application(
        handlers=[
            ('/', UserInfoHandler),
            ('/media/upload', MediaUploadHandler),
            ('/menu/update', MenuUpdateHandler),
            ('/group_id', UserGroupHandler),
        ],
        debug=True,
    )
    app.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
