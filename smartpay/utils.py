import re
import jtd

from .schemas.checkout_payload import checkout_payload_schema

public_key_pattern = re.compile("^pk_(test|live)_[0-9a-zA-Z]+$")
secret_key_pattern = re.compile("^sk_(test|live)_[0-9a-zA-Z]+$")
order_id_pattern = re.compile("^order_[0-9a-zA-Z]+$")


def is_valid_public_api_key(apiKey):
    return bool(public_key_pattern.match(apiKey))


def is_valid_secret_api_key(apiKey):
    return bool(secret_key_pattern.match(apiKey))


def is_valid_order_id(orderId):
    return bool(order_id_pattern.match(orderId))


def is_valid_vheckout_payload(payload):
    return jtd.validate(schema=checkout_payload_schema, instance=payload)


def normalize_checkout_payload(input):
    payload = dict(input)

    if not payload.get('currency'):
        payload['currency'] = payload.get('lineItems')[0].get('currency')

    if not payload.get('amount'):
        def get_price(item):
            if item.get('currency') != payload.get('currency'):
                raise Exception('Currency of all items should be the same.')

            return item.get('price')

        payload['amount'] = sum(map(get_price, payload.get('lineItems')))

    return payload
