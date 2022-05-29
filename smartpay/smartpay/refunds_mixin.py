from ..utils import valid_payment_id, valid_refund_id

from .base import GET, POST, PATCH


class RefundsMixin:
    REJECT_REQUEST_BY_CUSTOMER = 'requested_by_customer'
    REJECT_FRAUDULENT = 'fraudulent'

    def create_refund(self, payment=None, amount=None, currency=None, reason=None, reference=None, description=None, metadata=None):
        if not payment:
            raise Exception('Payment Id is required.')

        if not valid_payment_id(payment):
            raise Exception('Payment Id is invalid.')

        if not amount:
            raise Exception('Refund Amount is required.')

        if not currency:
            raise Exception('Refund Amount Currency is required.')

        if not reason:
            raise Exception('Refund Reason is required.')

        payload = {
            'payment': payment,
            'amount': amount,
            'currency': currency,
            'reason': reason,
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/refunds', POST, payload=payload)

    def refund(self, **kwargs):
        return self.create_refund(**kwargs)

    def get_refund(self, id=None, expand=None):
        if not id:
            raise Exception('Refund Id is required.')

        if not valid_refund_id(id):
            raise Exception('Refund ID is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/refunds/%s' % id, GET, params)

    def update_refund(self, id=None, reference=None, description=None, metadata=None):
        if not id:
            raise Exception('Refund Id is required.')

        if not valid_refund_id(id):
            raise Exception('Refund ID is invalid.')

        payload = {
            'reference': reference,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/refunds/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None})

    def list_refunds(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/refunds', GET, params)
