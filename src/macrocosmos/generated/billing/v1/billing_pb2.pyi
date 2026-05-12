from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetUsageRequest(_message.Message):
    __slots__ = ("product_type",)
    PRODUCT_TYPE_FIELD_NUMBER: _ClassVar[int]
    product_type: str
    def __init__(self, product_type: _Optional[str] = ...) -> None: ...

class BillingRate(_message.Message):
    __slots__ = ("rate_type", "unit_size", "unit_type", "price_per_unit", "currency")
    RATE_TYPE_FIELD_NUMBER: _ClassVar[int]
    UNIT_SIZE_FIELD_NUMBER: _ClassVar[int]
    UNIT_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRICE_PER_UNIT_FIELD_NUMBER: _ClassVar[int]
    CURRENCY_FIELD_NUMBER: _ClassVar[int]
    rate_type: str
    unit_size: int
    unit_type: str
    price_per_unit: float
    currency: str
    def __init__(self, rate_type: _Optional[str] = ..., unit_size: _Optional[int] = ..., unit_type: _Optional[str] = ..., price_per_unit: _Optional[float] = ..., currency: _Optional[str] = ...) -> None: ...

class SubscriptionInfo(_message.Message):
    __slots__ = ("external_id", "plan_code", "plan_tier", "free_allowance_usd", "free_allowance_remaining_usd", "usage_in_usd")
    EXTERNAL_ID_FIELD_NUMBER: _ClassVar[int]
    PLAN_CODE_FIELD_NUMBER: _ClassVar[int]
    PLAN_TIER_FIELD_NUMBER: _ClassVar[int]
    FREE_ALLOWANCE_USD_FIELD_NUMBER: _ClassVar[int]
    FREE_ALLOWANCE_REMAINING_USD_FIELD_NUMBER: _ClassVar[int]
    USAGE_IN_USD_FIELD_NUMBER: _ClassVar[int]
    external_id: str
    plan_code: str
    plan_tier: int
    free_allowance_usd: float
    free_allowance_remaining_usd: float
    usage_in_usd: float
    def __init__(self, external_id: _Optional[str] = ..., plan_code: _Optional[str] = ..., plan_tier: _Optional[int] = ..., free_allowance_usd: _Optional[float] = ..., free_allowance_remaining_usd: _Optional[float] = ..., usage_in_usd: _Optional[float] = ...) -> None: ...

class GetUsageResponse(_message.Message):
    __slots__ = ("available_credits", "used_credits", "remaining_credits", "billing_rates", "active_subscription")
    AVAILABLE_CREDITS_FIELD_NUMBER: _ClassVar[int]
    USED_CREDITS_FIELD_NUMBER: _ClassVar[int]
    REMAINING_CREDITS_FIELD_NUMBER: _ClassVar[int]
    BILLING_RATES_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_SUBSCRIPTION_FIELD_NUMBER: _ClassVar[int]
    available_credits: float
    used_credits: float
    remaining_credits: float
    billing_rates: _containers.RepeatedCompositeFieldContainer[BillingRate]
    active_subscription: SubscriptionInfo
    def __init__(self, available_credits: _Optional[float] = ..., used_credits: _Optional[float] = ..., remaining_credits: _Optional[float] = ..., billing_rates: _Optional[_Iterable[_Union[BillingRate, _Mapping]]] = ..., active_subscription: _Optional[_Union[SubscriptionInfo, _Mapping]] = ...) -> None: ...

class ChargeUserForUsageRequest(_message.Message):
    __slots__ = ("transaction_id", "channel", "rows")
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    transaction_id: str
    channel: str
    rows: int
    def __init__(self, transaction_id: _Optional[str] = ..., channel: _Optional[str] = ..., rows: _Optional[int] = ...) -> None: ...

class ChargeUserForUsageResponse(_message.Message):
    __slots__ = ("charge_cents", "transaction_id", "channel", "rows")
    CHARGE_CENTS_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    charge_cents: float
    transaction_id: str
    channel: str
    rows: int
    def __init__(self, charge_cents: _Optional[float] = ..., transaction_id: _Optional[str] = ..., channel: _Optional[str] = ..., rows: _Optional[int] = ...) -> None: ...

class UserHasEnoughAllowanceAndCreditsRequest(_message.Message):
    __slots__ = ("channel", "rows")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    channel: str
    rows: int
    def __init__(self, channel: _Optional[str] = ..., rows: _Optional[int] = ...) -> None: ...

class UserHasEnoughAllowanceAndCreditsResponse(_message.Message):
    __slots__ = ("has_enough", "charge_cents", "channel", "rows")
    HAS_ENOUGH_FIELD_NUMBER: _ClassVar[int]
    CHARGE_CENTS_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    has_enough: bool
    charge_cents: float
    channel: str
    rows: int
    def __init__(self, has_enough: bool = ..., charge_cents: _Optional[float] = ..., channel: _Optional[str] = ..., rows: _Optional[int] = ...) -> None: ...
