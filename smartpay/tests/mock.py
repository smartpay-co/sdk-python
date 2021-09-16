import json
import unittest

import httpretty
from httpretty import httprettified

from smartpay import Smartpay

API_PREFIX = 'https://api.smartpay.re/smartpayments'
CHECKOUT_URL = 'https://checkout.smartpay.re'

TEST_SECRET_KEY = 'sk_test_a7SlBkzf44tzdQoTwm6FrW'
TEST_PUBLIC_KEY = 'pk_test_1m2ySnST0aYi6QM0GlKP0n'

FAKE_SESSION = {
    'id': 'checkout_live_abcdef12345678',
}


class TestBasic(unittest.TestCase):
    @httprettified(allow_net_connect=False)
    def test_create_checkout_session(self):
        httpretty.register_uri(
            httpretty.POST,
            "%s/checkout/sessions" % (API_PREFIX, ),
            body=json.dumps(FAKE_SESSION)
        )

        smartpay = Smartpay(TEST_SECRET_KEY, api_prefix=API_PREFIX,
                            checkout_url='CHECKOUT_URL')

        payload = {
            "items": [
                {
                    "name": 'レブロン 18 LOW',
                    "price": 19250,
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
        }

        session = smartpay.create_checkout_session(payload)

        self.assertEqual(FAKE_SESSION.get('id'), session.get('id'))

        req = httpretty.last_request()

        self.assertEqual(req.headers['Authorization'],
                         'Basic %s' % (TEST_SECRET_KEY,),)

    def test_get_session_url(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY, checkout_url=CHECKOUT_URL)

        session_url = smartpay.get_session_url(FAKE_SESSION)

        self.assertTrue(session_url.index(CHECKOUT_URL) == 0)
        self.assertTrue(session_url.index('key=%s' % (TEST_PUBLIC_KEY, )) > 0)
        self.assertTrue(session_url.index('session=%s' %
                        (FAKE_SESSION.get('id'),)) > 0)
