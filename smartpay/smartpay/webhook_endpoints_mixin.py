from ..utils import valid_webhook_endpoint_id

from .base import GET, POST, PATCH, DELETE


class WebhookEndpointsMixin:
    def create_webhook_endpoint(self, url=None, description=None, event_subscriptions=None, metadata=None):
        if not url:
            raise Exception('URL is required.')

        payload = {
            'url': url,
            'description': description,
            'eventSubscriptions': event_subscriptions,
            'metadata': metadata,
        }

        return self.request('/webhook-endpoints', POST, payload=payload)

    def get_webhook_endpoint(self, id=None, expand=None):
        if not id:
            raise Exception('Webhook Endpoint Id is required.')

        if not valid_webhook_endpoint_id(id):
            raise Exception('Webhook Endpoint Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/webhook-endpoints/%s' % id, GET, params)

    def update_webhook_endpoint(self, id=None, url=None, description=None, event_subscriptions=None, metadata=None, active=None):
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

        return self.request('/webhook-endpoints/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None})

    def delete_webhook_endpoint(self, id=None):
        if not id:
            raise Exception('Webhook Endpoint Id is required.')

        if not valid_webhook_endpoint_id(id):
            raise Exception('Webhook Endpoint Id is invalid.')

        return self.request('/webhook-endpoints/%s' % id, DELETE)

    def list_webhook_endpoints(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/webhook-endpoints', GET, params)
