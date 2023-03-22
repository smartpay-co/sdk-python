# Smartpay Python SDK Reference

- [Class Smartpay](#class-smartpay)
  - [Constructor](#constructor)
  - [Create Checkout Session](#create-checkout-session)
  - [Get Checkout Session](#get-checkout-session)
  - [List Checkout Sessions](#list-checkout-sessions)
  - [Get Checkout Session URL](#get-checkout-session-url)
  - [Get Order](#get-order)
  - [Create Order With Token](#create-order)
  - [Cancel Order](#cancel-order)
  - [List Orders](#list-orders)
  - [Create Payment](#create-payment)
  - [Get Payment](#get-payment)
  - [Update Payment](#update-payment)
  - [List Payments](#list-payments)
  - [Create Refund](#create-refund)
  - [Get Refund](#get-refund)
  - [Update Refund](#update-refund)
  - [List Refunds](#list-refunds)
  - [Create Webhook Endpoint](#create-webhook-endpoint)
  - [Get Webhook Endpoint](#get-webhook-endpoint)
  - [Update Webhook Endpoint](#update-webhook-endpoint)
  - [Delete Webhook Endpoint](#delete-webhook-endpoint)
  - [List Webhook Endpoints](#list-webhook-endpoints)
  - [Calculate Webhook Signature](#calculate-webhook-signature)
  - [Verify Webhook Signature](#verify-webhook-signature)
  - [Webhook Express Middleware](#webhook-express-middleware)
  - [Create Coupon](#create-coupon)
  - [Get Coupon](#get-coupon)
  - [Update Coupon](#update-coupon)
  - [List Coupons](#list-coupons)
  - [Create Promotion Code](#create-promotion-code)
  - [Get Promotion Code](#get-promotion-code)
  - [Update Promotion Code](#update-promotion-code)
  - [List Promotion Codes](#list-promotion-codes)
  - [Get Token](#get-token)
  - [List Tokens](#list-tokens)
  - [Enable Token](#enable-token)
  - [Disable Token](#disable-token)
  - [Delete Token](#delete-token)
- [Collection](#collection)
  - [Properties](#properties)
- [Constants](#constants)
  - [Address Type](#address-type)
  - [Capture Method](#capture-method)
  - [Order Status](#order-status)
  - [Cancel Remainder](#cancel-remainder)
  - [Refund Reason](#refund-reason)
  - [Discount Type](#discount-type)
- [Common Exceptions](#common-exceptions)

## Class Smartpay

The main class.

### Constructor

```python
smartpay = Smartpay(
    secret_key=TEST_SECRET_KEY, public_key=TEST_PUBLIC_KEY)
```

#### Arguments

| Name                  | Type   | Description                            |
| --------------------- | ------ | -------------------------------------- |
| secret_key            | String | The secret key from merchant dashboard |
| public_key (optional) | String | The public key from merchant dashboard |

#### Return

Smartpay class instance. Methods documented below.

#### Exceptions

| Type  | Description            |
| ----- | ---------------------- |
| Error | Secret Key is required |
| Error | Secret Key is invalid  |
| Error | Public Key is invalid  |

### Create Checkout Session

Create a checkout session.

```python
session = smartpay.create_checkout_session(payload=payload)
```

#### Arguments

| Name    | Type   | Description                                                                      |
| ------- | ------ | -------------------------------------------------------------------------------- |
| payload | Object | The checkout session payload, [strict][strict-payload] or [loose][loose-payload] |

[strict-payload]: https://ja.docs.smartpay.co/reference/create-a-checkout-session
[loose-payload]: https://github.com/smartpay-co/sdk-node/blob/main/docs/SimpleCheckoutSession.md

#### Return

The [checkout session object][]

### Get Checkout Session

get single checkout session object by checkout session id.

```python
checkout_session = smartpay.get_checkout_session(id=session_id)
```

#### Arguments

| Name | Type   | Description             |
| ---- | ------ | ----------------------- |
| id   | String | The checkout session id |

#### Return

[Checkout session object][]

#### Exceptions

[Common exceptions][]

### List Checkout Sessions

List checkout session objects.

```python
checkout_sessions_collection = smartpay.list_checkout_sessions(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [checkout session object][]

#### Exceptions

[Common exceptions][]

### Get Checkout Session URL

Return the checkout URL of the checkout session.

```python
url = smartpay.get_session_url(session=session, promotion_code=promotion_code)
```

#### Arguments

| Name                      | Type   | Description                              |
| ------------------------- | ------ | ---------------------------------------- |
| session                   | String | The checkout session object              |
| promotion_code (optional) | String | The promotion code which will auto apply |

#### Return

The checkout URL of the checkout session. ex:

```
https://checkout.smartpay.co/checkout_live_vptIEMeycBuKLNNVRL6kB2.1ntK1e.2Z9eoI1j1KU7Jz7XMA9t9wU6gKI4ByzfUSJcwZAhYDoZWPr46ztb1F1ZcsBc7J4QmifNzmcNm4eVHSO98sMVzg
```

### Get Order

Get single order object by order id.

```python
order = smartpay.get_order(id=order_id)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The order id |

#### Return

[Order object][]

#### Exceptions

[Common exceptions][]

### Create Order

Create an order using a token.

```python
smartpay.create_order(id=order_id)
```

#### Arguments

| Name           | Type             | Description                |
| -------------- | ---------------- | -------------------------- |
| payload        | Array            | The [order payload][]      |
| idempotencyKey | String, optional | The custom idempotency key |

[order payload]: https://en.docs.smartpay.co/reference/create-order

#### Return

[Order object][]

### Cancel Order

Cancel an order.

```python
smartpay.cancel_order(id=order_id)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The order id |

#### Return

[Order object][]

#### Exceptions

[Common exceptions][]

### List Orders

List order objects.

```python
orders_collection = smartpay.list_orders(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [order object][]

#### Exceptions

[Common exceptions][]

### Create Payment

Create a payment object([capture][]) to an order.

```python
payment = smartpay.create_payment(
  order=order_id,
  amount=amount,
  currency=currency,
  cancel_remainder=cancel_remainder,
  reference=reference,
  description=description,
  line_items=line_items,
  metadata=metadata,
)
```

#### Arguments

| Name                                           | Type     | Description                                                                                              |
| ---------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------- |
| order                                          | String   | The order id                                                                                             |
| amount                                         | Number   | The amount of the payment                                                                                |
| currency                                       | String   | Three-letter ISO currency code, in uppercase. Must be a supported currency.                              |
| cancel_remainder (optional, default=automatic) | Stirng   | Whether to cancel remaining amount in case of a partial capture. `automatic` or `manual`.                |
| reference (optional)                           | String   | A string to reference the Payment which can be used to reconcile the Payment with your internal systems. |
| description (optional)                         | String   | An arbitrary long form explanation of the Payment, meant to be displayed to the customer.                |
| line_items (optional)                          | String[] | A list of the IDs of the Line Items of the original Payment this Refund is on.                           |
| metadata (optional)                            | Object   | Set of up to 20 key-value pairs that you can attach to the object.                                       |

#### Return

[Payment object][]

#### Exceptions

[Common exceptions][]

| Type          | Error Code                 | Description                                                           |
| ------------- | -------------------------- | --------------------------------------------------------------------- |
| SmartpayError | `order.not-found`          | No order was found meeting the requirements.                          |
| SmartpayError | `order.cannot-capture`     | No payment can be created. The error message will include the reason. |
| SmartpayError | `payment.excessive-amount` | The payment exceeds the order's amount available for capture          |

### Get Payment

Get the payment object by payment id.

```python
payment = smartpay.get_payment(id=payment_id)
```

#### Arguments

| Name | Type   | Description    |
| ---- | ------ | -------------- |
| id   | String | The payment id |

#### Return

[Payment object][]

#### Exceptions

[Common exceptions][]

### Update Payment

Create a payment object([capture][]) to an order.

```python
payment = smartpay.update_payment(
  id=payment_id,
  reference=reference,
  description=description,
  metadata=metadata
)
```

#### Arguments

| Name                   | Type   | Description                                                                                              |
| ---------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| id                     | String | The order id                                                                                             |
| reference (optional)   | String | A string to reference the Payment which can be used to reconcile the Payment with your internal systems. |
| description (optional) | String | An arbitrary long form explanation of the Payment, meant to be displayed to the customer.                |
| metadata (optional)    | Object | Set of up to 20 key-value pairs that you can attach to the object.                                       |

#### Return

[Payment object][]

#### Exceptions

[Common exceptions][]

### List Payments

List the payment objects.

```python
payments = smartpay.list_payments(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [payment object][]

#### Exceptions

[Common exceptions][]

### Create Refund

Create a refund object([refund][]) to a payment.

```python
refund = smartpay.create_refund(
  payment=payment_id,
  amount=amount,
  currency=currency,
  reason=reason,
  line_items=line_items,
  reference=reference,
  description=description,
  metadata=metadata,
)
```

#### Arguments

| Name                   | Type     | Description                                                                                              |
| ---------------------- | -------- | -------------------------------------------------------------------------------------------------------- |
| payment                | String   | The payment id                                                                                           |
| amount                 | Number   | The amount of the refund                                                                                 |
| currency               | String   | The order id                                                                                             |
| reason                 | Stirng   | The reason of the Refund. `requested_by_customer` or `fraudulent`                                        |
| line_items (optional)  | String[] | A list of the IDs of the Line Items of the original Payment this Refund is on.                           |
| reference (optional)   | String   | A string to reference the Payment which can be used to reconcile the Payment with your internal systems. |
| description (optional) | String   | An arbitrary long form explanation of the Payment, meant to be displayed to the customer.                |
| metadata (optional)    | Object   | Set of up to 20 key-value pairs that you can attach to the object.                                       |

#### Return

[Refund object][]

#### Exceptions

[Common exceptions][]

| Type          | Error Code            | Description                                                        |
| ------------- | --------------------- | ------------------------------------------------------------------ |
| SmartpayError | `payment.not-found`   | No payment was found meeting the requirements.                     |
| SmartpayError | `amount.insufficient` | Available amount on payment is insufficient to handle the request. |

### Get Refund

Get the refund object by refund id.

```python
refund = smartpay.get_refund(
  id=refund_id,
)
```

#### Arguments

| Name | Type   | Description   |
| ---- | ------ | ------------- |
| id   | String | The refund id |

#### Return

[Refund object][]

#### Exceptions

[Common exceptions][]

### Update Refund

Update a refund object([capture][]).

```python
refund = smartpay.update_refund(
  id=refund_id,
  reference=reference,
  description=description,
  metadata=metadata
)
```

#### Arguments

| Name                   | Type   | Description                                                                                              |
| ---------------------- | ------ | -------------------------------------------------------------------------------------------------------- |
| id                     | String | The refund id                                                                                            |
| reference (optional)   | String | A string to reference the Payment which can be used to reconcile the Payment with your internal systems. |
| description (optional) | String | An arbitrary long form explanation of the Payment, meant to be displayed to the customer.                |
| metadata (optional)    | Object | Set of up to 20 key-value pairs that you can attach to the object.                                       |

#### Return

[Refund object][]

#### Exceptions

[Common exceptions][]

### List Refunds

List refunds.

```python
refunds = smartpay.list_refunds(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [refund object][]

### Create Webhook Endpoint

Create a webhook endpoint object.

```python
webhook_endpoint = smartpay.create_webhook_endpoint(
  url=url,
  event_subscriptions=event_subscriptions,
  description=description,
  metadata=metadata,
)
```

#### Arguments

| Name                   | Type     | Description                                                                                        |
| ---------------------- | -------- | -------------------------------------------------------------------------------------------------- |
| url                    | String   | The url which will be called when any of the events you subscribed to occur.                       |
| event_subscriptions    | String[] | The list of events to subscribe to. If not specified you will be subsribed to all events.          |
| description (optional) | String   | An arbitrary long form explanation of the Webhook Endpoint, meant to be displayed to the customer. |
| metadata (optional)    | Object   | Set of up to 20 key-value pairs that you can attach to the object.                                 |

#### Return

[Webhook Endpoint object][]

#### Exceptions

[Common exceptions][]

### Get Webhook Endpoint

Get the webhook endpoint object by webhook endpoint id.

```python
webhook_endpoint = smartpay.get_webhook_endpoint(
  id=webhook_endpoint_id,
)
```

#### Arguments

| Name | Type   | Description             |
| ---- | ------ | ----------------------- |
| id   | String | The webhook endpoint id |

#### Return

[Webhook Endpoint object][]

#### Exceptions

[Common exceptions][]

### Update Webhook Endpoint

Update a webhook endpoint.

```python
webhook_endpoint = smartpay.update_webhook_endpoint(
  id=webhook_endpoint_id,
  active=active,
  url=url,
  event_subscriptions=event_subscriptions,
  description=description,
  metadata=metadata,
)
```

#### Arguments

| Name                           | Type     | Description                                                                                        |
| ------------------------------ | -------- | -------------------------------------------------------------------------------------------------- |
| id                             | String   | The order id                                                                                       |
| active (optional)              | Boolean  | Has the value true if the webhook endpoint is active and events are sent to the url specified.     |
| url (optional)                 | String   | The url which will be called when any of the events you subscribed to occur.                       |
| event_subscriptions (optional) | String[] | The list of events to subscribe to. If not specified you will be subsribed to all events.          |
| description (optional)         | String   | An arbitrary long form explanation of the Webhook Endpoint, meant to be displayed to the customer. |
| metadata (optional)            | Object   | Set of up to 20 key-value pairs that you can attach to the object.                                 |

#### Return

[Webhook Endpoint object][]

#### Exceptions

[Common exceptions][]

### Delete Webhook Endpoint

Delete the webhook endpoint by webhook endpoint id.

```python
smartpay.delete_webhook_endpoint(id=webhook_endpoint_id)
```

#### Arguments

| Name | Type   | Description             |
| ---- | ------ | ----------------------- |
| id   | String | The webhook endpoint id |

#### Return

Empty response body with 204

#### Exceptions

[Common exceptions][]

### List Webhook Endpoints

List the webhook endpoint objects.

```python
webhook_endpoints = smartpay.list_webhook_endpoints(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [webhook endpoint object][]

#### Exceptions

[Common exceptions][]

### Calculate Webhook Signature

Calculate the signature for webhook event of the given data.

```python
signature = smartpay.calculate_webhook_signature(
  data=data,
  secret=secret,
)
```

#### Arguments

| Name   | Type   | Description                       |
| ------ | ------ | --------------------------------- |
| data   | String | The data string                   |
| secret | String | The Base62 encoded signing secret |

#### Return

Signature of the data.

### Verify Webhook Signature

Verify the signature of the given data.

```python
signature = smartpay.verify_webhook_signature(
  data=data,
  secret=secret,
  signature=signature,
)
```

#### Arguments

| Name      | Type   | Description                       |
| --------- | ------ | --------------------------------- |
| data      | String | The data string                   |
| secret    | String | The Base62 encoded signing secret |
| signature | String | The expected signature value      |

#### Return

Boolean value, `true` if the signatures are matching.

### Create Coupon

create a coupon object.

```python
coupon = smartpay.create_coupon(
  name=name,
  currency=currency,
  discount_type=discount_type,
  discount_amount=discount_amount,
  discount_percentage=discount_percentage,
  expires_at=expires_at,
  max_redemption_count=max_redemption_count,
  metadata=metadata,
)
```

#### Arguments

| Name                            | Type   | Description                                                                                                        |
| ------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------ |
| name                            | String | The coupon's name, meant to be displayable to the customer.                                                        |
| discount_type                   | String | Discount Type. `amount` or `percentage`                                                                            |
| discount_amount                 | Number | Required if discount_type is `amount`. The amount of this coupon object.                                           |
| discount_percentage             | Number | Required if discount_type is `percentage`. The discount percentage of this coupon object.                          |
| currency                        | String | Required if discount_type is `amount`. Three-letter ISO currency code, in uppercase. Must be a supported currency. |
| expires_at (optional)           | String | Time at which the Coupon expires. Measured in milliseconds since the Unix epoch.                                   |
| max_redemption_count (optional) | String | Maximum number of times this coupon can be redeemed, in total, across all customers, before it is no longer valid. |
| metadata (optional)             | Object | Set of up to 20 key-value pairs that you can attach to the object.                                                 |

#### Return

[Coupon object][]

#### Exceptions

[Common exceptions][]

### Get Coupon

Get the coupon object by coupon id.

```python
coupon = smartpay.get_coupon(
  id=coupon_id,
)
```

#### Arguments

| Name | Type   | Description   |
| ---- | ------ | ------------- |
| id   | String | The coupon id |

#### Return

[Coupon object][]

#### Exceptions

[Common exceptions][]

### Update Coupon

Update a coupon.

```python
coupon = smartpay.update_coupon(
  active=active,
  name=name,
  metadata=metadata,
)
```

#### Arguments

| Name                | Type    | Description                                                                          |
| ------------------- | ------- | ------------------------------------------------------------------------------------ |
| id                  | String  | The coupon id                                                                        |
| name (optional)     | String  | The coupon's name, meant to be displayable to the customer.                          |
| active (optional)   | Boolean | Has the value true if the coupon is active and events are sent to the url specified. |
| metadata (optional) | Object  | Set of up to 20 key-value pairs that you can attach to the object.                   |

#### Return

[Coupon object][]

#### Exceptions

[Common exceptions][]

### List Coupons

List the coupon objects.

```python
coupons = smartpay.list_coupons(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [coupon object][]

#### Exceptions

[Common exceptions][]

### Create Promotion Code

Create a promotion code object of a coupon.

```python
promotion_code = smartpay.create_promotion_code(
  coupon=coupon_id,
  code=code,
  active=active,
  currency=currency,
  expires_at=expires_at,
  first_time_transaction=first_time_transaction
  one_per_customer=one_per_customer
  max_redemption_count=max_redemption_count,
  minimum_amount=minimum_amount,
  metadata=metadata,
)
```

#### Arguments

| Name                              | Type    | Description                                                                                                                                                    |
| --------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| coupon                            | String  | The unique identifier for the Coupon object.                                                                                                                   |
| code                              | String  | The customer-facing code. Regardless of case, this code must be unique across all your promotion codes.                                                        |
| active (optional)                 | Boolean | Has the value true (default) if the promotion code is active and can be used, or the value false if it is not.                                                 |
| currency (optional)               | String  | Three-letter ISO currency code, in uppercase. Must be a supported currency.                                                                                    |
| expires_at (optional)             | Number  | Time at which the Promotion Code expires. Measured in milliseconds since the Unix epoch.                                                                       |
| first_time_transaction (optional) | Boolean | A Boolean indicating if the Promotion Code should only be redeemed for customers without any successful order with the merchant. Defaults to false if not set. |
| max_redemption_count (optional)   | Number  | Maximum number of times this Promotion Code can be redeemed, in total, across all customers, before it is no longer valid.                                     |
| minimum_amount (optional)         | Number  | The minimum amount required to redeem this Promotion Code (e.g., the amount of the order must be ¥10,000 or more to be applicable).                            |
| one_per_customer (optional)       | Boolean | A Boolean indicating if the Promotion Code should only be redeemed once by any given customer. Defaults to false if not set.                                   |
| metadata (optional)               | Object  | Set of up to 20 key-value pairs that you can attach to the object.                                                                                             |

#### Return

[Promotion Code object][]

#### Exceptions

[Common exceptions][]

| Type          | Error Code              | Description                                                                                               |
| ------------- | ----------------------- | --------------------------------------------------------------------------------------------------------- |
| SmartpayError | `coupon.not-found`      | No coupon was found meeting the requirements.                                                             |
| SmartpayError | `promotion-code.exists` | The promotion code {code} already exists. The code needs to be unique across all of your promotion codes. |

### Get Promotion Code

get the promotion code object by promotion code id.

```python
promotion_code = smartpay.get_promotion_code(
  id=promotion_code_id,
)
```

#### Arguments

| Name | Type   | Description           |
| ---- | ------ | --------------------- |
| id   | String | The promotion code id |

#### Return

[Promotion Code object][]

#### Exceptions

[Common exceptions][]

### Update Promotion Code

Update a promotion code.

```python
promotion_code = smartpay.update_promotion_code(
  id=promotion_code_id,
  active=active,
  metadata=metadata,
)
```

#### Arguments

| Name                | Type    | Description                                                                                 |
| ------------------- | ------- | ------------------------------------------------------------------------------------------- |
| id                  | String  | The order id                                                                                |
| active (optional)   | Boolean | Has the value true if the promotion codeis active and events are sent to the url specified. |
| metadata (optional) | Object  | Set of up to 20 key-value pairs that you can attach to the object.                          |

#### Return

[Promotion Code object][]

#### Exceptions

[Common exceptions][]

### List Promotion Codes

List the promotion code objects.

```python
promotion_codes = smartpay.list_promotion_codes(
  max_results=max_results,
  page_token=page_token,
  expand=expand,
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [promotion code object][]

#### Exceptions

[Common exceptions][]

### Get Token

Get the token object by coupon id.

```python
token = smartpay.get_token(
  id=token_id,
)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The token id |

#### Return

[Token object][]

#### Exceptions

[Common exceptions][]

### List Tokens

List the token objects.

```python
tokens = smartpay.list_tokens(
  max_results=max_results,
  page_token=page_token,
  expand=expand
)
```

#### Arguments

| Name                               | Type   | Description                                                                                |
| ---------------------------------- | ------ | ------------------------------------------------------------------------------------------ |
| max_results (optional, defualt=20) | Number | Number of objects to return.                                                               |
| page_token (optional)              | String | The token for the page of the collection of objects.                                       |
| expand (optional, default=no)      | String | Set to `all` if the references within the response need to be expanded to the full objects |

#### Return

[Collection][] of [token object][]

#### Exceptions

[Common exceptions][]

### Enable Token

Enable the token by token id.

```python
result = smartpay.enable_token(
  id=coupon_id,
)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The token id |

#### Return

Empty response body with 200

#### Exceptions

[Common exceptions][]

| Type          | Error Code        | Description                                                                                                                   |
| ------------- | ----------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| SmartpayError | `token.not-found` | No token was found meeting the requirements. Try to enable token under `requires_authorization` status throws this error too. |

### Disable Token

Disable the token by token id.

```python
result = smartpay.disable_token(
  id=token_id,
)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The token id |

#### Return

Empty response body with 200

#### Exceptions

[Common exceptions][]

| Type          | Error Code        | Description                                                                                                                    |
| ------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| SmartpayError | `token.not-found` | No token was found meeting the requirements. Try to disable token under `requires_authorization` status throws this error too. |

### Delete Token

delete the token by token id.

```python
result = smartpay.delete_token(id=token_id)
```

#### Arguments

| Name | Type   | Description  |
| ---- | ------ | ------------ |
| id   | String | The token id |

#### Return

Empty response body with 204

#### Exceptions

[Common exceptions][]

| Type          | Error Code        | Description                                  |
| ------------- | ----------------- | -------------------------------------------- |
| SmartpayError | `token.not-found` | No token was found meeting the requirements. |

## Collection

Collection of items, a general data structure of collection data.

### Properties

| Name          | Type   | Description                                                                                                                        |
| ------------- | ------ | ---------------------------------------------------------------------------------------------------------------------------------- |
| object        | String | Always be `collection`                                                                                                             |
| pageToken     | String | The token for the page of the collection of objects.                                                                               |
| nextPageToken | String | The token for the next page of the collection of objects.                                                                          |
| maxResults    | Number | The maximum number of objects returned for this call. Equals to the maxResults query parameter specified (or 20 if not specified). |
| results       | Number | The actual number of objects returned for this call. This value is less than or equal to maxResults.                               |
| data          | Array  | The array of data                                                                                                                  |

## Constants

### Address Type

```
Smartpay.ADDRESS_TYPE_HOME
Smartpay.ADDRESS_TYPE_GIFT
Smartpay.ADDRESS_TYPE_LOCKER
Smartpay.ADDRESS_TYPE_OFFICE
Smartpay.ADDRESS_TYPE_STORE
```

### Capture Method

```
Smartpay.CAPTURE_METHOD_AUTOMATIC
Smartpay.CAPTURE_METHOD_MANUAL
```

### Order Status

```
Smartpay.ORDER_STATUS_SUCCEEDED
Smartpay.ORDER_STATUS_CANCELED
Smartpay.ORDER_STATUS_REJECTED
Smartpay.ORDER_STATUS_FAILED
Smartpay.ORDER_STATUS_REQUIRES_AUTHORIZATION
```

### Token Status

```
Smartpay.TOKEN_STATUS_ACTIVE
Smartpay.TOKEN_STATUS_DISABLED
Smartpay.TOKEN_STATUS_REJECTED
Smartpay.TOKEN_STATUS_REQUIRES_AUTHORIZATION
```

### Cancel Remainder

```
Smartpay.CANCEL_REMAINDER_AUTOMATIC
Smartpay.CANCEL_REMAINDER_MANUAL
```

### Refund Reason

```
Smartpay.REFUND_REQUEST_BY_CUSTOMER
Smartpay.REFUND_FRAUDULENT
```

### Discount Type

```
Smartpay.COUPON_DISCOUNT_TYPE_AMOUNT
Smartpay.COUPON_DISCOUNT_TYPE_PERCENTAGE
```

## Common Exceptions

| Type          | Error Code                   | Description                    |
| ------------- | ---------------------------- | ------------------------------ |
| SmartpayError | `unexpected_error`           | Unexpected network issue.      |
| SmartpayError | `unexpected_error`           | Unable to parse response body. |
| SmartpayError | `request.invalid`            | Required argument is missing.  |
| SmartpayError | Error code from API response | Unable to parse response body. |

[checkout session object]: https://en.docs.smartpay.co/reference/the-checkout-session-object
[order object]: https://en.docs.smartpay.co/reference/the-order-object
[payment object]: https://en.docs.smartpay.co/reference/the-payment-object
[refund object]: https://en.docs.smartpay.co/reference/the-refund-object
[webhook endpoint object]: https://en.docs.smartpay.co/reference/the-webhook-endpoint-object
[coupon object]: https://en.docs.smartpay.co/reference/the-coupon-object
[promotion code object]: https://en.docs.smartpay.co/reference/the-promotion-code-object
[token object]: https://en.docs.smartpay.co/reference/the-token-object
[capture]: https://en.docs.smartpay.co/docs/capture-an-order#using-the-smartpay-api
[refund]: https://en.docs.smartpay.co/docs/refund-a-purchase#using-the-smartpay-api
[collection]: #collection
[common exceptions]: #common-exceptions
