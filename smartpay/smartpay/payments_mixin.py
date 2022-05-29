from ..utils import valid_order_id, valid_payment_id

from .base import GET, POST


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
            raise Exception('Payment ID is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/payments/%s' % id, GET, params)
