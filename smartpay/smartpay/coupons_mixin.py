from ..utils import valid_coupon_id

from .base import GET, POST, PATCH

COUPON_DISCOUNT_TYPE_AMOUNT = 'amount'
COUPON_DISCOUNT_TYPE_PERCENTAGE = 'percentage'


class CouponsMixin:
    COUPON_DISCOUNT_TYPE_AMOUNT = COUPON_DISCOUNT_TYPE_AMOUNT
    COUPON_DISCOUNT_TYPE_PERCENTAGE = COUPON_DISCOUNT_TYPE_PERCENTAGE

    def create_coupon(self, name=None, currency=None, description=None, discount_amount=None, discount_percentage=None, discount_type=None, expires_at=None, max_redemption_count=None, metadata=None, idempotency_key=None):
        if not name:
            raise Exception('name is required.')

        if not discount_type:
            raise Exception('discount_type is required.')

        if discount_type != COUPON_DISCOUNT_TYPE_AMOUNT and discount_type != COUPON_DISCOUNT_TYPE_PERCENTAGE:
            raise Exception('discount_type is invalid.')

        if discount_type == COUPON_DISCOUNT_TYPE_AMOUNT and not discount_amount:
            raise Exception(
                'discount_amount is required if discount_type is amount.')

        if discount_type == COUPON_DISCOUNT_TYPE_AMOUNT and not currency:
            raise Exception(
                'currency is required if discount_amount is provided.')

        if discount_type == COUPON_DISCOUNT_TYPE_PERCENTAGE and not discount_percentage:
            raise Exception(
                'discount_percentage is required if discount_type is percentage.')

        payload = {
            'name': name,
            'currency': currency,
            'description': description,
            'discountAmount': discount_amount,
            'discountPercentage': discount_percentage,
            'discountType': discount_type,
            'expiresAt': expires_at,
            'maxRedemptionCount': max_redemption_count,
            'metadata': metadata,
        }

        return self.request('/coupons', POST, payload=payload, idempotency_key=idempotency_key)

    def get_coupon(self, id=None, expand=None):
        if not id:
            raise Exception('Coupon Id is required.')

        if not valid_coupon_id(id):
            raise Exception('Coupon Id is invalid.')

        params = {
            'expand': expand,
        }

        return self.request('/coupons/%s' % id, GET, params)

    def update_coupon(self, id=None, active=None, name=None, description=None, metadata=None, idempotency_key=None):
        if not id:
            raise Exception('Coupon Id is required.')

        if not valid_coupon_id(id):
            raise Exception('Coupon Id is invalid.')

        payload = {
            'active': active,
            'name': name,
            'description': description,
            'metadata': metadata,
        }

        return self.request('/coupons/%s' % id, PATCH, payload={k: v for k, v in payload.items() if v is not None}, idempotency_key=idempotency_key)

    def list_coupons(self, page_token=None, max_results=None, expand=None):
        params = {
            'pageToken': page_token,
            'maxResults': max_results,
            'expand': expand,
        }

        return self.request('/coupons', GET, params)
