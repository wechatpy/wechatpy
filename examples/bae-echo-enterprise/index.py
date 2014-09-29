# -*- coding:utf-8 -*-
from bae.core.wsgi import WSGIApplication

from wechatapp import app

application = WSGIApplication(app)
