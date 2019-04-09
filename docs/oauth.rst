.. _oauth:

微信 OAuth 网页授权接入
==================================

公众号 OAuth 网页授权接入
-----------------------------------

.. module:: wechatpy.oauth

.. autoclass:: WeChatOAuth
   :members:
   :inherited-members:

微信开放平台 代公众号 OAuth 网页授权接入
-----------------------------------

.. module:: wechatpy.component

.. autoclass:: ComponentOAuth
   :members:
   :inherited-members:

企业微信 OAuth 网页授权接入
-----------------------------------

下述代码使用 Flask_. 框架作为示例

.. _Flask: http://flask.pocoo.org

.. code-block:: python

    from flask import Flask, request, redirect, jsonify, session, abort
    from wechatpy.enterprise import WeChatClient
    import functools


    app = Flask(__name__)

    CORP_ID = 'wxc480d56d906bc121'
    SECRET = '79BAUPuQ0zcytpz7f5vouAFPwnWDK0XePjKeWsY7Wo-cpAZvYYAy0OH-PH0-6OUN'

    app.secret_key = 'key'

    client = WeChatClient(
        CORP_ID,
        SECRET
    )


    def oauth(method):
        @functools.wraps(method)
        def warpper(*args, **kwargs):
            code = request.args.get('code', None)
            url = client.oauth.authorize_url(request.url)

            if code:
                try:
                    user_info = client.oauth.get_user_info(code)
                except Exception as e:
                    print e.errmsg, e.errcode
                    # 这里需要处理请求里包含的 code 无效的情况
                    abort(403)
                else:
                    session['user_info'] = user_info
            else:
                return redirect(url)

            return method(*args, **kwargs)
        return warpper


    @app.route('/')
    @oauth
    def index():
        user_info = session.get('user_info')
        return jsonify(data=user_info)


    if __name__ == '__main__':
        app.run(
            debug=True,
            port=9000,
        )


.. module:: wechatpy.enterprise.client.api.oauth

.. autoclass:: WeChatOAuth
   :members:
   :inherited-members:
