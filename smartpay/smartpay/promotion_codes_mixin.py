from ..utils import valid_coupon_id, valid_promotion_code_id

from .base import GET, POST, PATCH


class PromotionCodesMixin:
    def create_promotion_code(self, coupon=None, code=None, active=None, currency=None, expires_at=None, first_time_transaction=None, one_per_customer=None, max_redemption_count=None, minimum_amount=None, metadata=None, idempotency_key=None):
        if not code:
            raise Exception('Code is required.')

        if not coupon:
            raise Exception('Coupon Id is required.')

        if not valid_coupon_id(coupon):
            raise Exception('Coupon Id is invalid.')

        if minimum_amount and not currency:
            raise Exception(
                'Currency is required if minimum_amount is provided.')

        payload = {
            'coupon': coupon,
            'code': code,
            'active': active,
            'currency': currency,
            'expiresAt': expires_at,
            'firstTimeTransaction': first_time_transaction,
            'onePerCustomer': one_per_customer,
            'maxRedemptionCount': max_redemption_count,
            'minimumAmount': minimum_amount,
            'metadata': metadata,
        }

        return self.request('/promotion-codes', POST, payload=payload, idempotency_key=idempotency_key)

    def get_promotion_code(self, id=None, expand=None):
        if not id:
            raise Exception('Promotion Code Id is required.')

        if not valid_promotion_code_id(id):
            raise Exception('Promotion Code Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/promotion-codes/%s' % id, GET, params)

    def update_promotion_code(self, id=None, active=None, metadata=None, idempotency_key=None):
        if not id:
            raise Exception('Promotion Code Id is required.')

        if not valid_promotion_code_id(id):
            raise Exception('Promotion Code Id is invalid.')

        payload = {
            'active': active,
            'metadata': metadata,
        }

        return self.request('/promotion-codes/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None}, idempotency_key=idempotency_key)

    def list_promotion_codes(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/promotion-codes', GET, params)
