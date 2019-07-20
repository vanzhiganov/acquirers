
import requests
from .exceptions import TinkoffException


class TinkoffBase(object):
    def __init__(self, terminal_id, password):
        self.terminal_id = terminal_id
        self.password = password


class TinkoffSimplePayment(TinkoffBase):
    def init(self, order_id, amount, ip=None, description=None, currency=None, token=None, language=None, customer_key=None, recurent=None, redirect_due_date=None, data=None, receipt=None):
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
        {'Success': False, 'ErrorCode': '9999', 'Message': 'Неверные параметры.', 'Details': 'Неверный токен. Проверьте пару TerminalKey/SecretKey.'}
        """
        data = dict()
        data['TerminalKey'] = self.terminal_id
        data['Amount'] = amount
        data['OrderId'] = order_id

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
    
    def cancel(self):
        """Cancel - отмена платежа
        Отменяет платёжную сессию. В зависимости от статуса платежа
        переводит его в следующие состояния
        """
        url = 'https://securepay.tinkoff.ru/v2/Cancel'
        return None
    
    def get_state(self):
        """Возвращает текуший статус платежа.
        """
        url = 'https://securepay.tinkoff.ru/v2/GetState'
    
    def resend(self):
        """Resend - отправка недоставленных нотификаций
        Метод предназначен для отправки всех неотправленных нотификаций,
        например, в случае недоступности в какой-либо момент времени сайта
        продавца.
        """
        url = 'https://securepay.tinkoff.ru/v2/Resend'


class TinkoffRecurrentPayment(TinkoffBase):
    def init(self):
        pass
    
    def charge(self):
        pass


class TinkoffCards(TinkoffBase):
    def add_customer(self):
        pass

    def get_customer(self):
        pass

    def remove_customer(self):
        pass

    def get_card_list(self):
        pass
