from ..utils import valid_token_id

from .base import GET, PUT, DELETE

TOKEN_STATUS_ACTIVE = 'active'
TOKEN_STATUS_DISABLED = 'disabled'
TOKEN_STATUS_REJECTED = 'rejected'
TOKEN_STATUS_REQUIRES_AUTHORIZATION = 'requires_authorization'


class TokensMixin:
    TOKEN_STATUS_ACTIVE = TOKEN_STATUS_ACTIVE
    TOKEN_STATUS_DISABLED = TOKEN_STATUS_DISABLED
    TOKEN_STATUS_REJECTED = TOKEN_STATUS_REJECTED
    TOKEN_STATUS_REQUIRES_AUTHORIZATION = TOKEN_STATUS_REQUIRES_AUTHORIZATION

    def get_token(self, id=None, expand=None):
        if not id:
            raise Exception('Token Id is required.')

        if not valid_token_id(id):
            raise Exception('Token Id is invalid.')

        return self.request('/tokens/%s' % id, GET)

    def enable_token(self, id=None, idempotency_key=None):
        if not id:
            raise Exception('Token Id is required.')

        if not valid_token_id(id):
            raise Exception('Token Id is invalid.')

        return self.request(
            '/tokens/%s/enable' % id, PUT, idempotency_key=idempotency_key
        )

    def disable_token(self, id=None, idempotency_key=None):
        if not id:
            raise Exception('Token Id is required.')

        if not valid_token_id(id):
            raise Exception('Token Id is invalid.')

        return self.request(
            '/tokens/%s/disable' % id, PUT, idempotency_key=idempotency_key
        )

    def delete_token(self, id=None, idempotency_key=None):
        if not id:
            raise Exception('Token Id is required.')

        if not valid_token_id(id):
            raise Exception('Token Id is invalid.')

        return self.request('/tokens/%s' % id, DELETE, idempotency_key=idempotency_key)

    def list_tokens(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/tokens', GET, params)
