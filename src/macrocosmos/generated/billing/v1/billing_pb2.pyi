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

class GetUsageResponse(_message.Message):
    __slots__ = ("available_credits", "used_credits", "remaining_credits", "billing_rates")
    AVAILABLE_CREDITS_FIELD_NUMBER: _ClassVar[int]
    USED_CREDITS_FIELD_NUMBER: _ClassVar[int]
    REMAINING_CREDITS_FIELD_NUMBER: _ClassVar[int]
    BILLING_RATES_FIELD_NUMBER: _ClassVar[int]
    available_credits: float
    used_credits: float
    remaining_credits: float
    billing_rates: _containers.RepeatedCompositeFieldContainer[BillingRate]
    def __init__(self, available_credits: _Optional[float] = ..., used_credits: _Optional[float] = ..., remaining_credits: _Optional[float] = ..., billing_rates: _Optional[_Iterable[_Union[BillingRate, _Mapping]]] = ...) -> None: ...
