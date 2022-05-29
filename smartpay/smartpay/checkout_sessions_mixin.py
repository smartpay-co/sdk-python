from urllib.parse import urlencode

from ..utils import valid_checkout_id
from ..utils import validate_checkout_session_payload, normalize_checkout_session_payload

from .base import GET, POST


class CheckoutSessionsMixin:
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

    def get_session_url(self, session, options={}):
        if not session:
            raise Exception('Checkout Session is required.')

        checkoutURL = session.get('url', None)
        promotionCode = options.get('promotionCode', None)

        if not checkoutURL:
            raise Exception('Checkout URL is not available.')

        params = {
            'promotion-code': promotionCode,
        }
        qs = urlencode([(key, params[key])
                       for key in params if params[key] is not None])

        if qs:
            return '%s?%s' % (checkoutURL, qs)

        return checkoutURL
