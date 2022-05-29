import json

from ..utils import valid_order_id, valid_payment_id

from .base import GET, POST, PATCH


class PaymentsMixin:
    def create_payment(self, order=None, amount=None, currency=None, cancel_remainder=None, reference=None, description=None, metadata=None):
        if not order:
            raise Exception('Order Id is required.')

        if not valid_order_id(order):
            raise Exception('Order ID is invalid.')

        if not amount:
            raise Exception('Payment Amount is required.')

        if not currency:
            raise Exception('Payment Amount Currency is required.')

        payload = {
            'order': order,
            'amount': amount,
            'currency': currency,
            'cancelRemainder': cancel_remainder,
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/payments', POST, payload=payload)

    def capture(self, **kwargs):
        return self.create_payment(**kwargs)

    def get_payment(self, id=None, expand=None):
        if not id:
            raise Exception('Payment Id is required.')

        if not valid_payment_id(id):
            raise Exception('Payment Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/payments/%s' % id, GET, params)

    def update_payment(self, id=None, reference=None, description=None, metadata=None):
        if not id:
            raise Exception('Payment Id is required.')

        if not valid_payment_id(id):
            raise Exception('Payment Id is invalid.')

        payload = {
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/payments/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None})

    def list_payments(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/payments', GET, params)
