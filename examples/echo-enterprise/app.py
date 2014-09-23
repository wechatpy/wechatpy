from __future__ import absolute_import, unicode_literals
from flask import Flask, request, abort
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException


TOKEN = '123456'
EncodingAESKey = ''
CorpId = ''

app = Flask(__name__)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echo_str = request.args.get('echostr', '')

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
    try:
        echo_str = crypto.check_signature(
            signature,
            timestamp,
            nonce,
            echo_str
        )
    except InvalidSignatureException:
        abort(403)
    if request.method == 'GET':
        return echo_str
    else:
        print('test')
        return ''


if __name__ == '__main__':
    app.run('127.0.0.1', 5001, debug=True)
