# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.4 
# Pydantic Version: 2.11.0 
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
