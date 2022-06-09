# Acquirers

![Python Acquirers](https://github.com/vanzhiganov/acquirers/raw/master/python-acquirers.png "Python Acquirers")

[![Acquirers at PYPI](https://img.shields.io/pypi/v/acquirers.svg)](https://pypi.org/project/Acquirers/)

## Who uses this module

- http://www.procdn.net
- http://www.gocloud.ru
- http://www.glavpodcast.ru
- http://www.zettadns.com

## Supported Acquirers

- [A-3](https://www.a-3.ru)
- [Tinkoff](https://oplata.tinkoff.ru/landing/develop/documentation/processing_payment)
- [Robokassa](https://robokassa.ru)

## Install

```shell
pip install Acquirers
```


## Tinkoff

API Documnetation: https://oplata.tinkoff.ru/landing/develop/documentation/processing_payment

```python
from Acquirers.Tinkoff import TinkoffSimplePayment

t = TinkoffSimplePayment(terminal_id, password)
t.init(tr.id, amount_tinkoff)
```

Result

```json
{
    "Success": true,
    "ErrorCode": "0",
    "TerminalKey": "1520095906182DEMO",
    "Status": "NEW",
    "PaymentId": "14458036",
    "OrderId": "02eb4dae-ec1e-44b2-844f-4e5c21e0bb88",
    "Amount": 100,
    "PaymentURL": "https://securepay.tinkoff.ru/pX81zg"
}
```

## Yandex.kassa

API Doc: https://kassa.yandex.ru/developers/api


## Rocketpay

```python
from Acquirers.Rocketpay import RocketpaySimplePayment

rp = RocketpaySimplePayment()
rp.merchant_id = '4'
rp.terminal_id = '4'
rp.secret_key = '265af92d-1ed8-433b-8c54-fa02a45f1227'
```

Инициируем платёж

```python
rp.init(order_id="example", amount="1.0")
```

