from .exceptions import TinkoffReceiptTaxationException


class Receipt(object):
    def __init__(self, taxation, email=None, phone=None):
        self.items = list()
        self.email = email
        self.phone = phone
        self.email_company = None
        self.taxation = self.set_taxation(taxation)

        if not email and not phone:
            pass

    def set_taxation(self, taxation: str) -> str:
        taxations_list = ['osn', 'usn_income', 'usn_income_outcome', 'envd', 'esn', 'patent']
        if taxation.lower() not in taxations_list:
            raise TinkoffReceiptTaxationException(taxation.lower())
        return taxation.lower()

    def set_item(self, name: str, price: int, quantity: int, amount: int, payment_method: str, payment_object: str, tax: str):
        self.items.append(ReceiptItem(name, price, quantity, amount, payment_method, payment_object, tax).__dict__())


class ReceiptItem(object):
    def __init__(self, name: str, price: int, quantity: int, amount: int, payment_method: str, payment_object: str, tax: str):
        self.name = name
        self.prince = price
        self.quantity = quantity
        self.amount = amount
        self.payment_method = payment_method
        self.payment_object = payment_object
        self.tax = tax

    def __dict__(self) -> dict:
        return {
            'Name': self.name,
            'Price': self.prince,
            'Quantity': self.quantity,
            'Amount': self.amount,
            'PaymentMethod': self.payment_method,
            'PaymentObject': self.payment_object,
            'Tax': self.tax
        }
