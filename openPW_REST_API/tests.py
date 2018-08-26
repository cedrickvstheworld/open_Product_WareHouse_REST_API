from django.test import TestCase
from django.test import TestCase
from urllib.request import urlopen
import json
from pprint import pprint
import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime


# Create your tests here.
# x = requests.get('http://localhost:8000/company/', auth=HTTPBasicAuth('cedie712', '123'))
#
# data = x.json()
#
# print(data)
#

# content ={
#     'user': 2,
#     'company_name': 'WalterMart',
#     'company_location': 'Gapan',
# }
#
# x = requests.get('http://localhost:8000/add_product/', auth=HTTPBasicAuth('monmon', '123'))
#
# print(x.content)

content = {
    'company': 1,
    'product_name': 'surf',
    'product_count': -600,
    'product_base_price': 35,
    'product_dispatch_price': 36,
    "product_description": "soap",
    "datetime_modified": str(datetime.now()),
}

x = requests.post('http://localhost:8000/product_trans/', data=content, auth=HTTPBasicAuth('cedie712', '123'))

print(x.content)