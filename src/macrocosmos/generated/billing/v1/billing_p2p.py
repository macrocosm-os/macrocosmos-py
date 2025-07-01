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
     ProductPlan is details of the subscription plan for a product
    """

# product_type: the type of the product (i.e. "gravity")
    rate_type: str = Field(default="")
# unit_size: the size of the unit of the subscription (e.g. 1000, 10000, 100000)
    unit_size: int = Field(default=0)
# unit_type: the type of the unit of the subscription (i.e. "rows")
    unit_type: str = Field(default="")
# price_per_unit: the price per unit of the subscription
    price_per_unit: float = Field(default=0.0)
# currency: the currency of the subscription
    currency: str = Field(default="")

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
