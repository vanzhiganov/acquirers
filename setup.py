from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='Acquirers',
    version='0.0.6',
    author="Vyacheslav Anzhiganov",
    author_email="vanzhiganov@yandex.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vanzhiganov/acquirers/",
    project_urls={
        "Source": "https://github.com/vanzhiganov/acquirers/",
        "Tracker": "https://github.com/vanzhiganov/acquirers/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
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
