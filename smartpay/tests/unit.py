import json
import unittest

import httpretty

from smartpay import Smartpay

API_PREFIX = 'https://api.smartpay.co/checkout'
CHECKOUT_URL = 'https://checkout.smartpay.co'

TEST_SECRET_KEY = 'sk_test_albwlejgsekcokfpdmva'
TEST_PUBLIC_KEY = 'pk_test_albwlejgsekcokfpdmva'

CODE = "FOO"

FAKE_SESSION = {
    'id': 'cs_live_abcdef12345678',
}


class TestBasic(unittest.TestCase):
    def test_payload_normalize(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY, checkout_url=CHECKOUT_URL)

        CODE1 = 'ABCDE12345'

        payload = {
            "currency": 'JPY',

            "items": [
                {
                    "name": 'Item',
                    "price": 100,
                    "quantity": 2,
                },
            ],

            "shipping": {
                "line1": 'line1',
                "locality": 'locality',
                "postalCode": '123',
                "country": 'JP',
            },

            "reference": 'order_ref_1234567',
            "successUrl": 'https://smartpay.co',
            "cancelUrl": 'https://smartpay.co',

            "promotionCode": CODE1,
        }

        normalizePayload = smartpay.normalize_checkout_session_payload(payload)

        self.assertTrue(normalizePayload.get(
            'orderData').get('amount') == 200)

    def test_get_session_url(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY, checkout_url=CHECKOUT_URL)

        session_url = smartpay.get_session_url(FAKE_SESSION, {
            'promotionCode': CODE
        })

        self.assertTrue(session_url.index(CHECKOUT_URL) == 0)
        self.assertTrue(session_url.index('public-key=%s' %
                        (TEST_PUBLIC_KEY, )) > 0)
        self.assertTrue(session_url.index('session-id=%s' %
                        (FAKE_SESSION.get('id'),)) > 0)
        self.assertTrue(session_url.index('promotion-code=%s' % CODE) > 0)
