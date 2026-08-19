from wechatpy.crypto import BasePrpCrypto, BaseWeChatCrypto
from wechatpy.work.exceptions import InvalidCorpIdException


class PrpCrypto(BasePrpCrypto):
    def encrypt(self, text, corp_id):
        return self._encrypt(text, corp_id)

    def decrypt(self, text, corp_id):
        return self._decrypt(text, corp_id, InvalidCorpIdException)


class WeChatCrypto(BaseWeChatCrypto):
    def __init__(self, token, encoding_aes_key, corp_id):
        super(WeChatCrypto, self).__init__(token, encoding_aes_key, corp_id)
        self.corp_id = corp_id

    def check_signature(self, signature, timestamp, nonce, echo_str):
        return self._check_signature(signature, timestamp, nonce, echo_str, PrpCrypto)

    def encrypt_message(self, msg, nonce, timestamp=None):
        return self._encrypt_message(msg, nonce, timestamp, PrpCrypto)

    def decrypt_message(self, msg, signature, timestamp, nonce):
        return self._decrypt_message(msg, signature, timestamp, nonce, PrpCrypto)
