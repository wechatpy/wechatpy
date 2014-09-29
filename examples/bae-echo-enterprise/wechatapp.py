from __future__ import absolute_import, unicode_literals
from flask import Flask, request, abort
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.enterprise.exceptions import InvalidCorpIdException
from wechatpy.enterprise import parse_message, create_reply


TOKEN = ''
EncodingAESKey = ''
CorpId = ''

app = Flask(__name__)


@app.route('/wechat', methods=['GET', 'POST'])
def wechat():
    signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')

    crypto = WeChatCrypto(TOKEN, EncodingAESKey, CorpId)
    if request.method == 'GET':
        echo_str = request.args.get('echostr', '')
        try:
            echo_str = crypto.check_signature(
                signature,
                timestamp,
                nonce,
                echo_str
            )
        except InvalidSignatureException:
            abort(403)
        return echo_str
    else:
        try:
            msg = crypto.decrypt_message(
                request.data,
                signature,
                timestamp,
                nonce
            )
        except (InvalidSignatureException, InvalidCorpIdException):
            abort(403)
        msg = parse_message(msg)
        if msg.type == 'text':
            reply = create_reply(msg.content, msg).render()
        else:
            reply = create_reply('Can not handle this for now', msg).render()
        res = crypto.encrypt_message(reply, nonce, timestamp)
        return res


if __name__ == '__main__':
    app.run('127.0.0.1', 5001, debug=True)
