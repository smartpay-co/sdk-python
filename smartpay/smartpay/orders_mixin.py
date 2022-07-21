from ..utils import valid_order_id

from .base import GET, PUT


class OrdersMixin:
    ORDER_STATUS_SUCCEEDED = 'succeeded'
    ORDER_STATUS_CANCELED = 'canceled'
    ORDER_STATUS_REJECTED = 'rejected'
    ORDER_STATUS_FAILED = 'failed'
    ORDER_STATUS_REQUIRES_AUTHORIZATION = 'requires_authorization'

    def list_orders(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/orders', GET, params)

    def get_order(self, id=None, expand=None):
        if not id:
            raise Exception('Order Id is required.')

        if not valid_order_id(id):
            raise Exception('Order ID is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/orders/%s' % id, GET, params)

    def cancel_order(self, id=None):
        if not id:
            raise Exception('Order Id is required.')

        if not valid_order_id(id):
            raise Exception('Order ID is invalid.')

        return self.request('/orders/%s/cancellation' % id, PUT)
