"""Acquirer"""
from hashlib import sha256
import requests
from .exceptions import TinkoffException, TinkoffSimplePaymentInitParameterRequiredException


class TinkoffBase(object):
    def __init__(self, terminal_id: str, password: str):
        self.terminal_id = terminal_id
        self.password = password

    def get_signature(self, data: dict) -> str:
        """Подпись запроса

        См. документацию: https://oplata.tinkoff.ru/landing/develop/documentation/request_sign

        >>> TinkoffBase('TinkoffBankTest', '123456').get_signature({"Amount":"100000", "Description":"test", "OrderId":"TokenExample", "Password":"123456", "TerminalKey":"TinkoffBankTest"})
        '597c160c8c348fb14c63c820c54b712468923a74fd111ac6b0ecda01fb5f4716'

        :param data:
        :return:
        """
        data_list = list()
        for d in sorted(list(data)):
            if d in ['Receipt', 'DATA']:
                continue
            data_list.append(data.get(d))
        return sha256(''.join(data_list).encode()).hexdigest()


class TinkoffSimplePayment(TinkoffBase):
    @staticmethod
    def _get_language(language: str) -> str:
        default = 'ru'
        if language.lower() not in ['ru', 'en']:
            return default
        else:
            return language.lower()

    @staticmethod
    def _is_recurrent(is_recurrent: bool) -> str:
        return 'y' if is_recurrent else 'n'

    def init(self, order_id, amount, ip=None, description=None, currency=None, language=None,
             customer_key=None, recurrent=False, redirect_due_date=None, data=None, receipt=None, sign_request=False):
        """Init - создание заказа

        :param:
        {
            'Success': True,
            'ErrorCode': '0',
            'TerminalKey': '1520095906182DEMO',
            'Status': 'NEW',
            'PaymentId': '14458036',
            'OrderId': '02eb4dae-ec1e-44b2-844f-4e5c21e0bb88',
            'Amount': 100,
            'PaymentURL': 'https://securepay.tinkoff.ru/pX81zg'
        }


        Errors:
        {
            'Success': False,
            'ErrorCode': '9999',
            'Message': 'Неверные параметры.',
            'Details': 'Неверный токен. Проверьте пару TerminalKey/SecretKey.'
        }
        """
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['Amount'] = amount
        data['OrderId'] = order_id

        if ip:
            data['IP'] = ip
        if description:
            data['Description'] = description
        if language:
            data['Language'] = self._get_language(language)
        if customer_key:
            data['CustomerKey'] = customer_key
        if recurrent:
            data['Recurrent'] = self._is_recurrent(recurrent)
            #
            if not data['CustomerKey']:
                raise TinkoffSimplePaymentInitParameterRequiredException('customer_key')
        if sign_request:
            data['Token'] = self.get_signature(data)

        request = requests.post('https://securepay.tinkoff.ru/v2/Init', json=data)
        data = request.json()

        if not data.get('Success'):
            raise TinkoffException(data)

        return data
    
    def finish_authorize(self,):
        """подтверждения платежа
        Данный метод используется, если магазин обладает сертификацией PCI DSS и использует свою
        собственную платёжную форму вместо формы банка. Метод FinishAuthorize подтверждает
        инициированный платёж передачей карточных данных. При использовании одностадийного
        проведения осуществляет списание денежных средств с карты покупателя. При двухстадийном
        проведении осуществляет блокировку указанной суммы на карте покупателя. 
        """
        return None
    
    def confirm(self):
        """Confirm - подтверждение платежа
        Подтверждает платёж и осуществляет списание заблокированных 
        ранее денежных средств.
        Используется при двухстадийном проведении платежа (при
        одностадийном проведении платежа вызывается автоматически).
        Применим только к платежам в статусе AUTHORIZED. Сумма
        подтверждения может быть меньше или равна сумме авторизации.
        Если сумма подтверждения меньше суммы платежа, будет выполнено
        частичное подтверждение.
        """
        url = 'https://securepay.tinkoff.ru/v2/Confirm'
        return None
    
    def cancel(self, payment_id):
        """Cancel - отмена платежа
        Отменяет платёжную сессию. В зависимости от статуса платежа
        переводит его в следующие состояния

        **Пример отправки запроса**
        {
            "TerminalKey":"TinkoffBankTest",
            "PaymentId":"2164657",
            "Token":"328a1ed43e3800c142b298fbb01772c739c524dd455717c8a9152428037439fb"
        }

        **Привет ответа**
        
        """
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['PaymentId'] = payment_id
        # data['IP'] = ip

        # Сумма отмены в копейках (**)
        # (*) в случае отмены платежа в статусах NEW или AUTHORIZED поле Amount,
        # даже если оно проставлено, игнорируется. Отмена из статусов NEW или AUTHORIZED
        # производится на полную сумму.
        # (**) в случае отмены платежа в статусе CONFIRMED, клиент может указать сумму
        # отмены явно. Если сумма отмены меньше суммы платежа, будет произведена 
        # частичная отмена. Частичную отмену можно производить до тех пор,
        # пока платёж не будет полностью отменён. На каждую отмену на Notifcation URL
        # будет отправляться нотификация CANCEL.
        # 
        # data['Amount'] = amount

        data['Token'] = self.get_signature(data)

        url = 'https://securepay.tinkoff.ru/v2/Cancel'
        request = requests.post(url, json=data)
        data = request.json()

        if not data.get('Success'):
            raise TinkoffException(data)

        return data
    
    def get_state(self, payment_id, amount=None, ip=None):
        """Возвращает текуший статус платежа.

        Пример отправки запроса
        {
         "TerminalKey":"TinkoffBankTest",
         "PaymentId":"2304882",
         "Token":"c0ad1dfc4e94ed44715c5ed0e84f8ec439695b9ac219a7a19555a075a3c3ed24"
        }

        Пример ответа
        {
         "Success": true,
         "ErrorCode": "0",
         "Message": "OK",
         "TerminalKey": "TinkoffBankTest",
         "Status": "DEADLINE_EXPIRED",
         "PaymentId": "2304882",
         "OrderId": "#419",
         "Amount": 1100
        }
        """
        url = 'https://securepay.tinkoff.ru/v2/GetState'

        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['PaymentId'] = payment_id
        if amount:
            data['Amount'] = amount
        if ip:
            data['IP'] = ip

        data['Token'] = self.get_signature(data)

        request = requests.post(url, json=data)
        data = request.json()

        if not data.get('Success'):
            raise TinkoffException(data)
        return data
    
    def resend(self):
        """Resend - отправка недоставленных нотификаций
        Метод предназначен для отправки всех неотправленных нотификаций,
        например, в случае недоступности в какой-либо момент времени сайта
        продавца.

        Response:

            {
                "Success":true,
                "ErrorCode":"0",
                "TerminalKey":"TestB",
                "Count":2
            }
        """
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['Token'] = self.get_signature(data)

        url = 'https://securepay.tinkoff.ru/v2/Resend'

        request = requests.post(url, json=data)
        response = request.json()

        return response


class TinkoffRecurrentPayment(TinkoffBase):
    """Рекуррентный платёж.
    По умолчанию рекуррентные платежи отключены.
    Для использования данного типа платежей обратитесь в банк.
    """

    def init(self, order_id, amount, customer_key, ip=None, description=None, currency=None,
             language=None, redirect_due_date=None, data=None, receipt=None, sign_request=False):
        simple = TinkoffSimplePayment(self.terminal_id, self.password)

        return simple.init(order_id, amount, ip, description, currency, language,
                           customer_key, True, redirect_due_date, data, receipt,
                           sign_request)

    def charge(self, payment_id, rebill_id, ip=None, send_email=False, info_email=None):
        url = "https://securepay.tinkoff.ru/v2/Charge"
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['PaymentId'] = payment_id
        if ip:
            data['IP'] = ip
        data['RebillId'] = rebill_id

        if send_email:
            data['SendEmail'] = send_email

        if info_email:
            # TODO: Обязателен при передаче SendEmail. Сделать проверку.
            data['InfoEmail'] = info_email

        data['Token'] = self.get_signature(data)

        request = requests.post(url, json=data)
        response = request.json()

        return response


class TinkoffCards(TinkoffBase):
    """Привязка и хранение карт"""

    def add_customer(self, customer_key: str, email=None, phone=None, ip=None) -> dict:
        """Данный метод регистрирует покупателя в системе и привязывает его к магазину Продавца.
        """
        url = "https://securepay.tinkoff.ru/v2/AddCustomer"
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['CustomerKey'] = customer_key
        if email:
            data['Email'] = email
        if phone:
            data['Phone'] = phone
        if ip:
            data['IP'] = ip

        request = requests.post(url, json=data)
        response = request.json()

        return response

    def get_customer(self, customer_key: str, ip=None) -> dict:
        url = "https://securepay.tinkoff.ru/v2/GetCustomer"
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['CustomerKey'] = customer_key
        if ip:
            data['IP'] = ip
        data['Token'] = self.get_signature(data)

        request = requests.post(url, json=data)
        response = request.json()

        return response

    def remove_customer(self, customer_key: str, ip=None) -> dict:
        """Удаляет данные покупателя

        :param customer_key:
        :param ip:
        :return:
        """
        url = "https://securepay.tinkoff.ru/v2/RemoveCustomer"

        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['CustomerKey'] = customer_key
        if ip:
            data['IP'] = ip
        data['Token'] = self.get_signature(data)

        request = requests.post(url, json=data)
        response = request.json()

        return response

    def get_card_list(self, customer_key: str, ip=None) -> dict:
        """Возвращает список привязанных карт у клиента, привязанного к магазину

        Ссылка на документацию: https://oplata.tinkoff.ru/landing/develop/documentation/GetCardList

        >>> TinkoffCards("TinkoffBankTest", "Password").get_card_list("Customer1")
        {
          "CardId": "881900",
          "Pan": "518223******0036",
          "Status": "D",
          "RebillId": " ",
          "CardType": 0,
          "ExpDate": "1122"
        },
        {
          "CardId": "882263",
          "Pan": "448744******4487",
          "Status": "A",
          "RebillId": " ",
          "CardType": 0,
          "ExpDate": "0619"
        }

        :param customer_key: str
        :param ip: str
        :return: dict
        """
        url = "https://securepay.tinkoff.ru/v2/GetCardList"

        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['CustomerKey'] = customer_key
        if ip:
            data['IP'] = ip
        data['Token'] = self.get_signature(data)

        request = requests.post(url, json=data)
        response = request.json()

        return response
