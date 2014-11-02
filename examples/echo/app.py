from __future__ import absolute_import, unicode_literals
import os
from flask import Flask, request, abort, render_template
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

# set token or get from environments
TOKEN = os.getenv('WECHAT_TOKEN', '123456')

app = Flask(__name__)


@app.route('/')
def index():
    host = request.url_root
    return render_template('index.html', host=host)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        return echo_str
    else:
        msg = parse_message(request.data)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg)
        else:
            reply = create_reply('Sorry, can not handle this for now', msg)
        return reply.render()


if __name__ == '__main__':
    app.run('127.0.0.1', 5001, debug=True)
