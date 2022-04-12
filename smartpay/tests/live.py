import os
import requests
import unittest
import warnings

from smartpay import Smartpay

unittest.TestLoader.sortTestMethodsUsing = None

API_BASE = os.environ.get('API_BASE', None)
TEST_SECRET_KEY = os.environ.get('SECRET_KEY', None)
TEST_PUBLIC_KEY = os.environ.get('PUBLIC_KEY', None)
TEST_USERNAME = os.environ.get('TEST_USERNAME', None)
TEST_PASSWORD = os.environ.get('TEST_PASSWORD', None)

test_session_data = {}


class TestBasic(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter('ignore', ResourceWarning)

    def test_0_create_checkout_session_loose_1(self):
        smartpay = Smartpay(TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY)

        CODE = 'ZOO'

        payload = {
            "currency": 'JPY',
            "items": [
                {
                    "name": 'レブロン 18 LOW',
                    "amount": 250,
                    "quantity": 1,
                },
            ],

            "shippingInfo": {
                "address": {
                    "line1": 'line1',
                    "locality": 'locality',
                    "postalCode": '123',
                    "country": 'JP',
                },

                "feeAmount": 100,
            },

            "captureMethod": 'manual',

            "successUrl": 'https://smartpay.co',
            "cancelUrl": 'https://smartpay.co',

            "promotionCode": CODE,
        }

        session = smartpay.create_checkout_session(payload)

        test_session_data['manual_capture_session'] = session

        self.assertTrue(len(session.get('id')) > 0)
        self.assertTrue(session.get('url').find(CODE) >= 0)

        print(session)

    def test_0_create_checkout_session_loose_2(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        payload = {
            "items": [
                {
                    "name": 'レブロン 18 LOW',
                    "amount": 250,
                    "currency": 'JPY',
                    "quantity": 1,
                },
            ],

            "shippingInfo": {
                "address": {
                    "line1": 'line1',
                    "locality": 'locality',
                    "postalCode": '123',
                    "country": 'JP',
                },

                "feeAmount": 100,
            },

            "captureMethod": 'manual',

            "reference": 'order_ref_1234567',
            "successUrl": 'https://smartpay.co',
            "cancelUrl": 'https://smartpay.co',
        }

        session = smartpay.create_checkout_session(payload)

        test_session_data['cancel_order_session'] = session

        self.assertTrue(len(session.get('id')) > 0)

    def test_0_get_orders(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        orders_collection = smartpay.get_orders(max_results=10)

        self.assertTrue(len(orders_collection.get('data')) > 0)

        next_page_token = orders_collection.get('nextPageToken')

        if next_page_token:
            next_orders_collection = smartpay.get_orders(
                page_token=next_page_token, max_results=10)

            self.assertTrue(len(next_orders_collection.get('data')) > 0)

        first_order = orders_collection.get('data')[0]

        order = smartpay.get_order(id=first_order.get('id'))

        self.assertTrue(order.get('id') == first_order.get('id'))

    def test_1_create_payment(self):
        order_id = test_session_data.get(
            'manual_capture_session').get('order').get('id')
        PAYMENT_AMOUNT = 50

        login_response = requests.request('POST', 'https://%s/consumers/auth/login' % (API_BASE, ), json={
            "emailAddress": TEST_USERNAME,
            "password": TEST_PASSWORD
        })
        login_response_data = login_response.json()
        access_token = login_response_data.get('accessToken', None)

        r = requests.request('POST', 'https://%s/orders/%s/authorizations' % (API_BASE, order_id), headers={
            'Authorization': 'Bearer %s' % (access_token,),
        }, json={
            "paymentMethod": "pm_test_visaApproved",
            "paymentPlan": "pay_in_three"
        })

        smartpay = Smartpay(TEST_SECRET_KEY)

        payment1 = smartpay.create_payment(
            order=order_id, amount=PAYMENT_AMOUNT, currency='JPY', cancel_remainder='manual')

        payment2 = smartpay.capture(
            order=order_id, amount=PAYMENT_AMOUNT + 1, currency='JPY', cancel_remainder='manual')

        self.assertTrue(payment1.get('id'))
        self.assertTrue(payment2.get('id'))
        self.assertTrue(payment2.get('amount') == PAYMENT_AMOUNT + 1)

        retrived_payment2 = smartpay.get_payment(payment2.get('id'))

        self.assertTrue(payment2.get('id') == retrived_payment2.get('id'))
        self.assertTrue(payment2.get('amount') ==
                        retrived_payment2.get('amount'))

    def test_2_create_refund(self):
        order_id = test_session_data.get(
            'manual_capture_session').get('order').get('id')
        REFUND_AMOUNT = 1

        smartpay = Smartpay(TEST_SECRET_KEY)

        order = smartpay.get_order(id=order_id)
        refundable_payment = order.get('payments')[0]

        refund1 = smartpay.create_refund(
            payment=refundable_payment, amount=REFUND_AMOUNT, currency='JPY', reason=Smartpay.REJECT_REQUEST_BY_CUSTOMER)

        refund2 = smartpay.refund(
            payment=refundable_payment, amount=REFUND_AMOUNT + 1, currency='JPY', reason=Smartpay.REJECT_REQUEST_BY_CUSTOMER)

        self.assertTrue(refund1.get('id'))
        self.assertTrue(refund2.get('id'))
        self.assertTrue(refund2.get('amount') == REFUND_AMOUNT + 1)

        retrived_refund2 = smartpay.get_refund(refund2.get('id'))

        self.assertTrue(refund2.get('id') == retrived_refund2.get('id'))
        self.assertTrue(refund2.get('amount') ==
                        retrived_refund2.get('amount'))

    def test_3_cancel_order(self):
        order_id = test_session_data.get(
            'cancel_order_session').get('order').get('id')

        login_response = requests.request('POST', 'https://%s/consumers/auth/login' % (API_BASE, ), json={
            "emailAddress": TEST_USERNAME,
            "password": TEST_PASSWORD
        })
        login_response_data = login_response.json()
        access_token = login_response_data.get('accessToken', None)

        r = requests.request('POST', 'https://%s/orders/%s/authorizations' % (API_BASE, order_id), headers={
            'Authorization': 'Bearer %s' % (access_token,),
        }, json={
            "paymentMethod": "pm_test_visaApproved",
            "paymentPlan": "pay_in_three"
        })

        smartpay = Smartpay(TEST_SECRET_KEY)

        result = smartpay.cancel_order(order_id)

        self.assertTrue(result.get('status') == 'canceled')
