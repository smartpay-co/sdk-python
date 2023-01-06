import hmac
import base62
import hashlib

from ..utils import valid_webhook_endpoint_id

from .base import GET, POST, PATCH, DELETE

BASE62 = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'


class WebhookEndpointsMixin:
    def create_webhook_endpoint(self, url=None, description=None, event_subscriptions=None, metadata=None, idempotency_key=None):
        if not url:
            raise Exception('URL is required.')

        payload = {
            'url': url,
            'description': description,
            'eventSubscriptions': event_subscriptions,
            'metadata': metadata,
        }

        return self.request('/webhook-endpoints', POST, payload=payload, idempotency_key=idempotency_key)

    def get_webhook_endpoint(self, id=None, expand=None):
        if not id:
            raise Exception('Webhook Endpoint Id is required.')

        if not valid_webhook_endpoint_id(id):
            raise Exception('Webhook Endpoint Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/webhook-endpoints/%s' % id, GET, params)

    def update_webhook_endpoint(self, id=None, url=None, description=None, event_subscriptions=None, metadata=None, active=None, idempotency_key=None):
        if not id:
            raise Exception('Webhook Endpoint Id is required.')

        if not valid_webhook_endpoint_id(id):
            raise Exception('Webhook Endpoint Id is invalid.')

        payload = {
            'url': url,
            'description': description,
            'eventSubscriptions': event_subscriptions,
            'metadata': metadata,
            'active': active
        }

        return self.request('/webhook-endpoints/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None}, idempotency_key=idempotency_key)

    def delete_webhook_endpoint(self, id=None, idempotency_key=None):
        if not id:
            raise Exception('Webhook Endpoint Id is required.')

        if not valid_webhook_endpoint_id(id):
            raise Exception('Webhook Endpoint Id is invalid.')

        return self.request('/webhook-endpoints/%s' % id, DELETE, idempotency_key=idempotency_key)

    def list_webhook_endpoints(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/webhook-endpoints', GET, params)

    def calculate_webhook_signature(self, data=None, secret=None):
        if not data:
            raise Exception('data is required.')

        if not secret:
            raise Exception('secret is required.')

        signer = hmac.new(base62.decodebytes(secret, charset=BASE62), msg=bytes(
            data, 'utf-8'), digestmod=hashlib.sha256)
        calculated_signature = signer.hexdigest()

        return calculated_signature

    def verify_webhook_signature(self, data=None, secret=None, signature=None):
        if not data:
            raise Exception('data is required.')

        if not secret:
            raise Exception('secret is required.')

        calculated_signature = self.calculate_webhook_signature(
            data=data,
            secret=secret,
        )

        return signature == calculated_signature
