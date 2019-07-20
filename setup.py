from setuptools import setup

setup(
    name='Acquirers',
    version='0.0.4',
    packages=[
        'Acquirers',
        'Acquirers.Tinkoff',
        'Acquirers.Rocketpay',
        'Acquirers.Yandexcheckout',
    ],
    install_requires=[
        'requests',
        'yandex_checkout',
    ]
)
