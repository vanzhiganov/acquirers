# Acquirers

```python
from Acquirers.Tinkoff import TinkoffSimplePayment

result = TinkoffSimplePayment(terminal_id, password).init(tr.id, amount_tinkoff)
```

Result

```json
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
```
