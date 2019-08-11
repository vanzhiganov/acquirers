
import hmac
from hashlib import md5
from hashlib import sha1
import requests
from .exceptions import RocketpayException


class RocketpayBase(object):
    def __init__(self, merchant_id=None, terminal_id=None, secret_key=None):
        self.url = 'http://proc.rocketpay.ru'
        self.merchant_id = merchant_id
        self.terminal_id = terminal_id
        self.secret_key = secret_key

    def sign_hmac(self, data):
        data_list = list()
        for d in sorted(list(data)):
            data_list.append(str(data.get(d)))
        return hmac.new(
            self.secret_key.encode(),
            ''.join(data_list).encode(),
            sha1
        ).hexdigest()


class RocketpaySimplePayment(RocketpayBase):
    def init(self, order_id, amount, email=None, phone=None):
        """
        
        >>> RocketpayPayment().init(**):
        """
        data = {
            "merchant_id": self.merchant_id,
            "terminal_id": self.terminal_id,
            "amount": amount,
            "order_id": order_id,
        }
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone

        data['sign'] = self.sign_hmac(data)

        response = requests.post(self.url + '/api/v1/process/init', json=data)

        if response.status_code not in [200, 201]:
            raise RocketpayException(response.json())

        return response.json()
