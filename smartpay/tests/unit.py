import unittest

from ..smartpay import Smartpay

from .utils.mock_retry_server import Mock_retry_server

API_PREFIX = 'https://api.smartpay.co/checkout'

TEST_SECRET_KEY = 'sk_test_albwlejgsekcokfpdmva'
TEST_PUBLIC_KEY = 'pk_test_albwlejgsekcokfpdmva'
CHECKOUT_URL = 'https://checkout.smartpay.co'

CODE = "FOO"

FAKE_SESSION = {
    'id': 'checkout_test_hm3tau0XY7r3ULm06pHtr8',
    'url': 'https://checkout.smartpay.co/checkout_test_hm3tau0XY7r3ULm06pHtr8.1nsIwu.9tR7VVYMmLWwq77hGPuN0HbPB6TYsPKLrJbJJkcIKiR8GUY0WalxEoRtBcWF6I1WYLGit6xiAlJtyi8xrXxDfD?demo=true&promotion-code=SPRINGSALE2022&',
}


class TestBasic(unittest.TestCase):
    def test_payload_normalize(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY)

        CODE1 = 'ABCDE12345'

        payload = {
            "currency": 'JPY',

            "items": [
                {
                    "name": 'Item',
                    "amount": 100,
                    "quantity": 2,
                },
            ],

            "shippingInfo": {
                "address": {
                    "line1": 'line1',
                    "locality": 'locality',
                    "postalCode": '123',
                    "country": 'JP',
                }
            },

            "reference": 'order_ref_1234567',
            "successUrl": 'https://smartpay.co',
            "cancelUrl": 'https://smartpay.co',

            "promotionCode": CODE1,
        }

        normalizePayload = smartpay.normalize_checkout_session_payload(payload)

        self.assertEqual(normalizePayload.get('amount'), 200)

    def test_get_session_url(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY)

        session_url = smartpay.get_session_url(FAKE_SESSION,
                                               promotion_code=CODE)

        self.assertTrue(session_url.index(CHECKOUT_URL) == 0)
        self.assertTrue(session_url.index('%s' %
                        (FAKE_SESSION.get('id'),)) > 0)
        self.assertTrue(session_url.index('promotion-code=%s' % CODE) > 0)

    def test_verify_webhook_signature(self):
        smartpay = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY)

        data = '1653028612220.{"id":"evt_test_dwPfFKu5iSEKyHR2LFj9Lx","object":"event","createdAt":1653028523052,"test":true,"eventData":{"type":"payment.created","version":"2022-02-18","data":{"id":"payment_test_35LxgmF5KM22XKG38BjpJg","object":"payment","test":true,"createdAt":1653028523020,"updatedAt":1653028523020,"amount":200,"currency":"JPY","order":"order_test_RiYq2rthzRHrkKVGeucSwn","reference":"order_ref_1234567","status":"processed","metadata":{}}}}'
        secret = 'gybcsjixKyBW2d4z6iNPlaYzHUMtawnodwZt3W0q'
        signature = '68007ada8485ea0ceca7c5e879ae860a50412b7af95ab8e81b32a3e13f3c0832'

        self.assertTrue(smartpay.verify_webhook_signature(
            data=data, secret=secret, signature=signature))

    def test_retry_policy(self):

        retry_server = Mock_retry_server()
        retry_server.init()

        smartpay1 = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY, api_prefix='http://127.0.0.1:3001', retries=5)

        res1 = smartpay1.request('/')

        self.assertEqual(res1, 'ok')

        smartpay2 = Smartpay(
            TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY, api_prefix='http://127.0.0.1:3001', retries=1)
        
        try:
            smartpay2.request('/')
            self.assertTrue(False)
        except:
            self.assertTrue(True)

