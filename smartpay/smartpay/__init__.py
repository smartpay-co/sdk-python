import os

from .checkout_sessions_mixin import CheckoutSessionsMixin
from .orders_mixin import OrdersMixin
from .payments_mixin import PaymentsMixin
from .refunds_mixin import RefundsMixin
from .webhook_endpoints_mixin import WebhookEndpointsMixin
from .coupons_mixin import CouponsMixin
from .promotion_codes_mixin import PromotionCodesMixin
from .tokens_mixin import TokensMixin

from ..utils import valid_public_api_key, valid_secret_api_key
from ..utils import retry_requests, nonce

from ..__version__ import __version__

API_PREFIX = 'https://api.smartpay.co/v1'

api_prefix_candidate = os.environ.get('SMARTPAY_API_PREFIX', None)

SMARTPAY_API_PREFIX = (
    api_prefix_candidate
    if api_prefix_candidate and 'api.smartpay' in api_prefix_candidate
    else None
)
SMARTPAY_SECRET_KEY = os.environ.get('SMARTPAY_SECRET_KEY', None)
SMARTPAY_PUBLIC_KEY = os.environ.get('SMARTPAY_PUBLIC_KEY', None)


class Smartpay(
    CheckoutSessionsMixin,
    OrdersMixin,
    PaymentsMixin,
    RefundsMixin,
    WebhookEndpointsMixin,
    CouponsMixin,
    PromotionCodesMixin,
    TokensMixin,
):
    def __init__(self, secret_key, public_key=None, api_prefix=None, retries=1):
        input_secret_key = secret_key or SMARTPAY_SECRET_KEY

        if not secret_key:
            raise Exception('Secret Key is required.')

        if not valid_secret_api_key(input_secret_key):
            raise Exception('Secret Key is invalid.')

        if public_key and not valid_public_api_key(public_key):
            raise Exception('Public Key is invalid.')

        self._secret_key = input_secret_key
        self._public_key = public_key or SMARTPAY_PUBLIC_KEY
        self._api_prefix = api_prefix or SMARTPAY_API_PREFIX or API_PREFIX
        self.requests_session = retry_requests(retries=retries)

    def request(
        self, endpoint, method='GET', params={}, payload=None, idempotency_key=None
    ):
        params['dev-lang'] = 'python'
        params['sdk-version'] = __version__

        r = self.requests_session.request(
            method,
            '%s%s' % (self._api_prefix, endpoint),
            headers={
                'Authorization': 'Basic %s' % (self._secret_key,),
                'Idempotency-Key': idempotency_key or nonce(),
            },
            params=params,
            json=payload,
        )

        if r.status_code < 200 or r.status_code > 299:
            raise Exception('%s: %s' % (r.status_code, r.text))

        if r.status_code == 204:
            return r.text

        content_type = r.headers.get('Content-Type', '').split(';')[0]

        if content_type == 'application/json' or content_type == 'text/json':
            return r.json()

        return r.text

    def set_public_key(self, public_key):
        if not public_key:
            raise Exception('Public API Key is required.')

        if not valid_public_api_key(public_key):
            raise Exception('Public API Key is invalid.')

        self._public_key = public_key
