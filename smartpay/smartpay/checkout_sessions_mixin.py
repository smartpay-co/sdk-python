from urllib.parse import urlencode

from ..utils import valid_checkout_id
from ..utils import validate_checkout_session_payload, normalize_checkout_session_payload

from .base import GET, POST

ADDRESS_TYPE_HOME = 'home'
ADDRESS_TYPE_GIFT = 'gift'
ADDRESS_TYPE_LOCKER = 'locker'
ADDRESS_TYPE_OFFICE = 'office'
ADDRESS_TYPE_STORE = 'store'

CAPTURE_METHOD_AUTOMATIC = 'autommatic'
CAPTURE_METHOD_MANUAL = 'manual'


class CheckoutSessionsMixin:
    ADDRESS_TYPE_HOME = ADDRESS_TYPE_HOME
    ADDRESS_TYPE_GIFT = ADDRESS_TYPE_GIFT
    ADDRESS_TYPE_LOCKER = ADDRESS_TYPE_LOCKER
    ADDRESS_TYPE_OFFICE = ADDRESS_TYPE_OFFICE
    ADDRESS_TYPE_STORE = ADDRESS_TYPE_STORE

    CAPTURE_METHOD_AUTOMATIC = CAPTURE_METHOD_AUTOMATIC
    CAPTURE_METHOD_MANUAL = CAPTURE_METHOD_MANUAL

    def normalize_checkout_session_payload(self, payload):
        normalize_payload = normalize_checkout_session_payload(payload)
        errors = validate_checkout_session_payload(normalize_payload)

        if len(errors) > 0:
            raise Exception(errors)

        return normalize_payload

    def create_checkout_session(self, payload):
        normalized_payload = self.normalize_checkout_session_payload(payload)

        session = self.request(
            '/checkout-sessions', POST,  payload=normalized_payload)

        try:
            session['url'] = self.get_session_url(session, {
                'promotionCode': payload.get('promotionCode', None)
            })
        except Exception:
            pass

        return session

    def get_checkout_session(self, id=None, expand=None):
        if not id:
            raise Exception('Checkout Session Id is required.')

        if not valid_checkout_id(id):
            raise Exception('Checkout Session Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/checkout-sessions/%s' % id, GET, params)

    def list_checkout_sessions(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/checkout-sessions', GET, params)

    def get_session_url(self, session, promotion_code=None, options={}):
        if not session:
            raise Exception('Checkout Session is required.')

        checkout_url = session.get('url', None)
        promotion_code = promotion_code or options.get('promotionCode', None)

        if not checkout_url:
            raise Exception('Checkout URL is not available.')

        params = {
            'promotion-code': promotion_code,
        }
        qs = urlencode([(key, params[key])
                       for key in params if params[key] is not None])

        if qs:
            return '%s?%s' % (checkout_url, qs)

        return checkout_url
