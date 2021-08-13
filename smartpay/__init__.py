import requests
from urllib.parse import urlencode

from .utils import is_valid_vheckout_payload, is_valid_public_api_key, is_valid_secret_api_key, is_valid_order_id, normalize_checkout_payload


API_PREFIX = 'https://api.smartpay.co/checkout'
CHECKOUT_URL = 'https://checkout.smartpay.ninja'

POST = 'POST'
PUT = 'PUT'

STATUS_SUCCEEDED = 'succeeded'


class Smartpay:
    def __init__(self, secret_key, public_key=None, api_prefix=API_PREFIX, checkout_url=CHECKOUT_URL):
        if not secret_key:
            raise Exception('Secret API Key is required.')

        if not is_valid_secret_api_key(secret_key):
            raise Exception('Secret API Key is invalid.')

        if public_key and not is_valid_public_api_key(public_key):
            raise Exception('Public API Key is invalid.')

        self._secret_key = secret_key
        self._public_key = public_key
        self._api_prefix = api_prefix
        self._checkout_url = checkout_url

    def request(self, endpoint, method='GET', payload=None):
        r = requests.request(method, '%s%s' % (self._api_prefix, endpoint), headers={
            'Authorization': 'Bearer %s' % (self._secret_key,),
        }, json=payload)

        if r.status_code >= 300:
            raise Exception(r.text)

        return r.json()

    def create_checkout_session(self, payload):
        if not is_valid_vheckout_payload(payload):
            raise Exception('Checkout Payload is invalid.')

        session = self.request(
            '/sessions', POST, normalize_checkout_payload(payload))

        try:
            session['checkoutURL'] = self.get_session_url(session)
        except Exception:
            pass

        return session

    def is_order_authorized(self, order_id):
        order = self.get_order(order_id)

        return order.get('status') == STATUS_SUCCEEDED

    def get_orders(self):
        return self.request('/orders')

    def get_order(self, order_id):
        if not is_valid_order_id(order_id):
            raise Exception('Order ID is invalid.')

        return self.request('/orders/%s' % order_id)

    # def captureOrder(self, order_id, amount):
    #     return self.request('/orders/%s/capture' % order_id, POST, json={'amount': amount})

    def refund_order(self, order_id, amount):
        return self.request('/orders/%s/refund' % order_id, POST, json={'amount': amount})

    # def cancelOrder(self, order_id):
    #     return self.request('/orders/%s/cancel' % order_id, POST)

    def set_public_key(self, public_key):
        if not public_key:
            raise Exception('Public API Key is required.')

        if not is_valid_public_api_key(public_key):
            raise Exception('Public API Key is invalid.')

        self._public_key = public_key

    def get_session_url(self, session):
        if not session:
            raise Exception('Checkout Session is required.')

        if not self._public_key:
            raise Exception('Public API Key is required.')

        params = {
            'session': session.get('id'),
            'key': self._public_key
        }

        return '%s/login?%s' % (self._checkout_url, urlencode(params))
