# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class GetUsageRequest(BaseModel):
    """
     GetUsageRequest is the request message for getting the usage of the user's credits
    """

# product_type: the type of the product (i.e. "gravity")
    product_type: typing.Optional[str] = Field(default="")

class BillingRate(BaseModel):
    """
     BillingRate is the billing rate for a product
    """

# rate_type: the type of the billing rate (i.e. "gravity")
    rate_type: str = Field(default="")
# unit_size: the size of the unit of the subscription (e.g. 1000, 10000, 100000)
    unit_size: int = Field(default=0)
# unit_type: the type of the unit of the subscription (i.e. "rows")
    unit_type: str = Field(default="")
# price_per_unit: the price per unit of the subscription
    price_per_unit: float = Field(default=0.0)
# currency: the currency of the subscription
    currency: str = Field(default="")

class SubscriptionInfo(BaseModel):
    """
     SubscriptionInfo contains the active subscription details
    """

# external_id: the external ID of the subscription
    external_id: str = Field(default="")
# plan_code: the plan code of the subscription
    plan_code: str = Field(default="")
# plan_tier: the tier of the plan (0=Free, 1=Astronaut, 2=Cosmonaut)
    plan_tier: int = Field(default=0)
# free_allowance_usd: the total free allowance in USD per month for the active subscription
    free_allowance_usd: float = Field(default=0.0)
# free_allowance_remaining_usd: the remaining free allowance in USD for the current period
    free_allowance_remaining_usd: float = Field(default=0.0)
# usage_in_usd: the current usage amount in USD for the billing period
    usage_in_usd: float = Field(default=0.0)

class GetUsageResponse(BaseModel):
    """
     GetUsageResponse is the response message for getting the usage of the user's credits
    """

# available_credits: the number of credits available to the user
    available_credits: float = Field(default=0.0)
# used_credits: the number of credits used by the user
    used_credits: float = Field(default=0.0)
# remaining_credits: the number of credits remaining to the user
    remaining_credits: float = Field(default=0.0)
# subscription: the subscription that the user has
    billing_rates: typing.List[BillingRate] = Field(default_factory=list)
# active_subscription: the currently active subscription
    active_subscription: typing.Optional[SubscriptionInfo] = Field(default_factory=SubscriptionInfo)

class ChargeUserForUsageRequest(BaseModel):
    """
     ChargeUserForUsageRequest is the request message for charging a user for usage
    """

# transaction_id: unique identifier for this transaction
    transaction_id: str = Field(default="")
# channel: the gravity service channel ("dataset" or "on_demand")
    channel: str = Field(default="")
# rows: the number of rows to charge for (can be negative for refunds)
    rows: int = Field(default=0)

class ChargeUserForUsageResponse(BaseModel):
    """
     ChargeUserForUsageResponse is the response message for charging a user for usage
    """

# charge_cents: the amount charged in cents
    charge_cents: float = Field(default=0.0)
# transaction_id: the transaction ID
    transaction_id: str = Field(default="")
# channel: the channel that was charged
    channel: str = Field(default="")
# rows: the number of rows charged
    rows: int = Field(default=0)

class UserHasEnoughAllowanceAndCreditsRequest(BaseModel):
    """
     UserHasEnoughAllowanceAndCreditsRequest is the request message for checking if a user has enough allowance and credits
    """

# channel: the gravity service channel ("dataset" or "on_demand")
    channel: str = Field(default="")
# rows: the number of rows to check for
    rows: int = Field(default=0)

class UserHasEnoughAllowanceAndCreditsResponse(BaseModel):
    """
     UserHasEnoughAllowanceAndCreditsResponse is the response message for checking if a user has enough allowance and credits
    """

# has_enough: whether the user has enough allowance and credits
    has_enough: bool = Field(default=False)
# charge_cents: the amount that would be charged in cents
    charge_cents: float = Field(default=0.0)
# channel: the channel that would be charged
    channel: str = Field(default="")
# rows: the number of rows that would be charged
    rows: int = Field(default=0)
