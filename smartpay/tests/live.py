import os
import json
import unittest

from smartpay import Smartpay

TEST_SECRET_KEY = 'sk_test_KTGPODEMjGTJByn1pu8psb'
TEST_PUBLIC_KEY = 'pk_test_7smSiNAbAwsI2HKQE9e3hA'


class TestBasic(unittest.TestCase):
    def test_create_checkout_session_loose_1(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        CODE = 'ZOO'

        payload = {
            "currency": 'JPY',
            "items": [
                {
                    "name": 'レブロン 18 LOW',
                    "price": 250,
                    "quantity": 1,
                },
            ],

            "shipping": {
                "line1": 'line1',
                "locality": 'locality',
                "postalCode": '123',
                "country": 'JP',

                "feeAmount": 100,
            },

            "reference": 'order_ref_1234567',
            "successURL": 'https://smartpay.co',
            "cancelURL": 'https://smartpay.co',

            "promotionCode": CODE,
        }

        session = smartpay.create_checkout_session(payload)

        print(session)

        self.assertTrue(len(session.get('id')) > 0)
        self.assertTrue(session.get('metadata').get(
            '__promotion_code__') == CODE)

    def test_create_checkout_session_loose_2(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

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

                "feeAmount": 100,
            },

            "reference": 'order_ref_1234567',
            "successURL": 'https://smartpay.co',
            "cancelURL": 'https://smartpay.co',
        }

        session = smartpay.create_checkout_session(payload)

        print(session)

        self.assertTrue(len(session.get('id')) > 0)

    def test_create_checkout_session_strict(self):
        smartpay = Smartpay(TEST_SECRET_KEY)

        payload = {
            "orderData": {
                "currency": 'JPY',

                "lineItemData": [
                    {
                        "priceData": {
                            "productData": {
                                "name": 'ナイキ エア ズーム テンポ ...',
                                "description": 'メンズ ランニングシューズ',
                                "images": ['https://i.ibb.co/vJRf12N/Item-image.png'],
                            },
                            "amount": 100,
                            "currency": 'JPY',
                        },
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
                    "feeCurrency": 'JPY',
                },
            },

            "customerInfo": {
                "emailAddress": 'john@smartpay.co',
                "firstName": 'John',
                "lastName": 'Doe',
                "firstNameKana": 'ジョン',
                "lastNameKana": 'ドエ',
                "phoneNumber": '+818000000000',
                "dateOfBirth": '2000-01-01',
                "legalGender": 'male',
                "address": {
                    "line1": 'line1',
                    "line2": 'line2',
                    "locality": '世田谷区',
                    "administrativeArea": '東京都',
                    "postalCode": '155-0031',
                    "country": 'JP',
                },
                "accountAge": 30,
            },

            "reference": 'order_ref_1234567',
            "successURL": 'https://smartpay.co',
            "cancelURL": 'https://smartpay.co',
        }

        session = smartpay.create_checkout_session(payload)

        print(session)

        self.assertTrue(len(session.get('id')) > 0)
