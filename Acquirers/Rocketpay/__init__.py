from hashlib import md5
import requests
from .exceptions import RocketpayException


class RocketpayBase(object):
    def __init__(self, merchant_id=None, secret_key=None):
        self.url = 'https://proc.rocketpay.ru'
        self.merchant_id = merchant_id
        self.secret_key = secret_key


class RocketpaySimplePayment(RocketpayBase):
    def init(self, order_id, amount):
        """
        
        >>> RocketpayPayment().init(**):
        """
        string = "{}:{}:{}:{}".format(
            self.merchant_id, amount, order_id, self.secret_key
        )

        sign = md5(string.encode()).hexdigest()
        data = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "order_id": order_id,
            "sign": sign,
            "email": "vanzhiganov@ya.ru",
        }

        response = requests.post(self.url + '/api/v1/process/init', json=data)

        if response.status_code != 201:
            raise RocketpayException(response.json())

        return response.json()
