import os
import json
import unittest

from smartpay import Smartpay

DOMNAIN_NAME = os.environ.get('DOMAIN_NAME', 'api.smartpay.co')

API_PREFIX = 'https://%s/smartpayments' % (DOMNAIN_NAME,)
CHECKOUT_URL = 'https://checkout.smartpay.co'

TEST_SECRET_KEY = 'sk_test_a7SlBkzf44tzdQoTwm6FrW'
TEST_PUBLIC_KEY = 'pk_test_1m2ySnST0aYi6QM0GlKP0n'


class TestBasic(unittest.TestCase):
    def test_create_checkout_session(self):
        smartpay = Smartpay(TEST_SECRET_KEY, api_prefix=API_PREFIX,
                            checkout_url='CHECKOUT_URL')

        payload = {
            "items": [
                {
                    "name": 'レブロン 18 LOW',
                    "price": 250,
                    "currency": 'JPY',
                    "quantity": 1,
                },
            ],

            "shipping": {
                "line1": 'line1',
                "locality": 'locality',
                "postalCode": '123',
                "country": 'JP',
            },

            "reference": 'order_ref_1234567',
            "successURL": 'https://smartpay.co',
            "cancelURL": 'https://smartpay.co',

            "test": True,
        }

        session = smartpay.create_checkout_session(payload)

        print(session)

        self.assertTrue(len(session.get('id')) > 0)
