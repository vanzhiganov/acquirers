from setuptools import setup

setup(
    name='Acquirers',
    version='0.0.2',
    packages=[
        'Acquirers',
        'Acquirers.Tinkoff',
        'Acquirers.Rocketpay',
    ],
    install_requires=[
        'requests'
    ]
)
