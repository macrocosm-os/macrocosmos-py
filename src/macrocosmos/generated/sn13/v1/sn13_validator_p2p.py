# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class ListTopicsRequest(BaseModel):
    """
     ListTopicsRequest is the request message for getting the top topics
    """

# source: the source to validate
    source: str = Field(default="")

class ListTopicsResponseDetail(BaseModel):
    """
     ListTopicsResponseDetail is the response message for getting the top topics
    """

# label_value: reddit or x topic
    label_value: str = Field(default="")
# content_size_bytes: content size in bytes
    content_size_bytes: int = Field(default=0)
# adj_content_size_bytes: adjacent content size in bytes
    adj_content_size_bytes: int = Field(default=0)

class ListTopicsResponse(BaseModel):
    """
     ListTopicsResponse is a list of ListTopicsResponseDetail(s) with top topics
    """

# message: the response message
    details: typing.List[ListTopicsResponseDetail] = Field(default_factory=list)

class ValidateRedditTopicRequest(BaseModel):
    """
     ValidateTopicRequest is the request message for validating a reddit topic
    """

# topic: the topic to validate
    topic: str = Field(default="")

class ValidateRedditTopicResponse(BaseModel):
    """
     ValidateTopicResponse is the response message for validating a topic
    """

# platform: i.e. reddit
    platform: str = Field(default="")
# topic: the topic to validate
    topic: str = Field(default="")
# exists: whether the topic exists
    exists: bool = Field(default=False)
# over18: whether the topic is NSFW
    over18: bool = Field(default=False)
# quarantine: whether the topic is quarantined
    quarantine: bool = Field(default=False)

class OnDemandDataRequest(BaseModel):
    """
     OnDemandDataRequest is a request to SN13 to retrieve data
    """

# source: the data source (X or Reddit)
    source: str = Field(default="")
# usernames: list of usernames to fetch data from
    usernames: typing.List[str] = Field(default_factory=list)
# keywords: list of keywords to search for
    keywords: typing.List[str] = Field(default_factory=list)
# start_date: ISO 8601 formatted date string (e.g. "2024-01-01T00:00:00Z")
    start_date: typing.Optional[str] = Field(default="")
# end_date: ISO 8601 formatted date string (e.g. "2024-01-31T23:59:59Z")
    end_date: typing.Optional[str] = Field(default="")
# limit: maximum number of results to return
    limit: typing.Optional[int] = Field(default=0)

class OnDemandDataResponse(BaseModel):
    """
     OnDemandDataResponse is the response from SN13 for an on-demand data request
    """

# status: the request status, either success/error
    status: str = Field(default="")
# data: the data object returned
    data: typing.List[typing.Dict[str, typing.Any]] = Field(default_factory=list)
# meta: additional metadata about the request
    meta: typing.Dict[str, typing.Any] = Field(default_factory=dict)
