import os
import time
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
                {
                    "kind": 'discount',
                    "name": 'discount',
                    "amount": 10,
                    "currency": 'JPY',
                },
                {
                    "kind": 'discount',
                    "name": 'discount',
                    "amount": 10,
                    "currency": 'JPY',
                },
                {
                    "kind": 'tax',
                    "name": 'tax',
                    "amount": 10,
                    "currency": 'JPY',
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
                    "amount": 350,
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

        retrived_session = smartpay.get_checkout_session(id=session.get('id'))

        self.assertTrue(session.get('id') == retrived_session.get('id'))

        sessions_collection = smartpay.list_checkout_sessions(max_results=10)

        self.assertTrue(len(sessions_collection.get('data')) > 0)

    def test_0_list_orders(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        orders_collection = smartpay.list_orders(max_results=10)

        self.assertTrue(len(orders_collection.get('data')) > 0)

        next_page_token = orders_collection.get('nextPageToken')

        if next_page_token:
            next_orders_collection = smartpay.list_orders(
                page_token=next_page_token, max_results=10)

            self.assertTrue(len(next_orders_collection.get('data')) > 0)

        first_order = orders_collection.get('data')[0]

        order = smartpay.get_order(id=first_order.get('id'))

        self.assertTrue(order.get('id') == first_order.get('id'))

    def test_1_create_payment(self):
        order_id = test_session_data.get(
            'manual_capture_session').get('order').get('id')
        PAYMENT_AMOUNT = 150

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

        updated_payment2 = smartpay.update_payment(
            id=payment2.get('id'), reference='updated')
        retrived_payment2 = smartpay.get_payment(payment2.get('id'))

        self.assertTrue(payment2.get('id') == retrived_payment2.get('id'))
        self.assertTrue(payment2.get('id') == updated_payment2.get('id'))
        self.assertTrue(payment2.get('amount') ==
                        retrived_payment2.get('amount'))
        self.assertTrue(retrived_payment2.get('reference') == 'updated')

        payments_collection = smartpay.list_payments()

        self.assertTrue(len(payments_collection.get('data')) > 0)

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

        updated_refund_2 = smartpay.update_refund(
            refund2.get('id'), reference='updated')
        retrived_refund2 = smartpay.get_refund(refund2.get('id'))

        self.assertTrue(refund2.get('id') == updated_refund_2.get('id'))
        self.assertTrue(refund2.get('id') == retrived_refund2.get('id'))
        self.assertTrue(refund2.get('amount') ==
                        retrived_refund2.get('amount'))
        self.assertTrue(updated_refund_2.get('reference') == 'updated')

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

    def test_4_webhook_crud(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        webhook_endpoint = smartpay.create_webhook_endpoint(
            url='https://smartpay.co',
            event_subscriptions=['merchant_user.created'],
        )

        updated_webhook_endpoint = smartpay.update_webhook_endpoint(
            id=webhook_endpoint.get('id'),
            description='updated'
        )

        retrived_webhook_endpoint = smartpay.get_webhook_endpoint(
            id=webhook_endpoint.get('id')
        )

        self.assertTrue(webhook_endpoint.get('id'))
        self.assertTrue(webhook_endpoint.get('id') ==
                        updated_webhook_endpoint.get('id'))
        self.assertTrue(retrived_webhook_endpoint.get(
            'description') == 'updated')

        webhook_endpoints_collection = smartpay.list_webhook_endpoints()

        self.assertTrue(len(webhook_endpoints_collection.get('data')) > 0)

        delete_result = smartpay.delete_webhook_endpoint(
            id=webhook_endpoint.get('id')
        )

        self.assertTrue(delete_result == '')

    def test_5_coupon_code_cru(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        # Coupon
        coupon = smartpay.create_coupon(
            name='E2E Test coupon',
            discount_type=Smartpay.COUPON_DISCOUNT_TYPE_AMOUNT,
            discount_amount=100,
            currency='JPY',
        )

        updated_coupon = smartpay.update_coupon(
            id=coupon.get('id'),
            name='updatedCoupon'
        )

        retrived_coupon = smartpay.get_coupon(
            id=coupon.get('id')
        )

        self.assertTrue(coupon.get('id'))
        self.assertTrue(coupon.get('id') == updated_coupon.get('id'))
        self.assertTrue(retrived_coupon.get('name') == 'updatedCoupon')

        coupons_collection = smartpay.list_coupons()

        self.assertTrue(len(coupons_collection.get('data')) > 0)

        # Promotion Code
        promotion_code = smartpay.create_promotion_code(
            coupon=updated_coupon.get('id'),
            code='THECODE%s' % (time.time(),),
        )

        updated_promotion_code = smartpay.update_promotion_code(
            id=promotion_code.get('id'),
            active=False
        )

        retrived_promotion_code = smartpay.get_promotion_code(
            id=promotion_code.get('id')
        )

        self.assertTrue(promotion_code.get('id'))
        self.assertTrue(promotion_code.get('id') ==
                        updated_promotion_code.get('id'))
        self.assertTrue(retrived_promotion_code.get('active') == False)

        promotion_codes_collection = smartpay.list_promotion_codes()

        self.assertTrue(len(promotion_codes_collection.get('data')) > 0)
