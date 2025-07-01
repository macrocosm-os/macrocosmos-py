from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListTopicsRequest(_message.Message):
    __slots__ = ("source",)
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    source: str
    def __init__(self, source: _Optional[str] = ...) -> None: ...

class ListTopicsResponseDetail(_message.Message):
    __slots__ = ("label_value", "content_size_bytes", "adj_content_size_bytes")
    LABEL_VALUE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    ADJ_CONTENT_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    label_value: str
    content_size_bytes: int
    adj_content_size_bytes: int
    def __init__(self, label_value: _Optional[str] = ..., content_size_bytes: _Optional[int] = ..., adj_content_size_bytes: _Optional[int] = ...) -> None: ...

class ListTopicsResponse(_message.Message):
    __slots__ = ("details",)
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    details: _containers.RepeatedCompositeFieldContainer[ListTopicsResponseDetail]
    def __init__(self, details: _Optional[_Iterable[_Union[ListTopicsResponseDetail, _Mapping]]] = ...) -> None: ...

class ValidateRedditTopicRequest(_message.Message):
    __slots__ = ("topic",)
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    topic: str
    def __init__(self, topic: _Optional[str] = ...) -> None: ...

class ValidateRedditTopicResponse(_message.Message):
    __slots__ = ("platform", "topic", "exists", "over18", "quarantine")
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    OVER18_FIELD_NUMBER: _ClassVar[int]
    QUARANTINE_FIELD_NUMBER: _ClassVar[int]
    platform: str
    topic: str
    exists: bool
    over18: bool
    quarantine: bool
    def __init__(self, platform: _Optional[str] = ..., topic: _Optional[str] = ..., exists: bool = ..., over18: bool = ..., quarantine: bool = ...) -> None: ...

class OnDemandDataRequest(_message.Message):
    __slots__ = ("source", "usernames", "keywords", "start_date", "end_date", "limit")
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    USERNAMES_FIELD_NUMBER: _ClassVar[int]
    KEYWORDS_FIELD_NUMBER: _ClassVar[int]
    START_DATE_FIELD_NUMBER: _ClassVar[int]
    END_DATE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    source: str
    usernames: _containers.RepeatedScalarFieldContainer[str]
    keywords: _containers.RepeatedScalarFieldContainer[str]
    start_date: str
    end_date: str
    limit: int
    def __init__(self, source: _Optional[str] = ..., usernames: _Optional[_Iterable[str]] = ..., keywords: _Optional[_Iterable[str]] = ..., start_date: _Optional[str] = ..., end_date: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class OnDemandDataResponse(_message.Message):
    __slots__ = ("status", "data", "meta")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    META_FIELD_NUMBER: _ClassVar[int]
    status: str
    data: _containers.RepeatedCompositeFieldContainer[_struct_pb2.Struct]
    meta: _struct_pb2.Struct
    def __init__(self, status: _Optional[str] = ..., data: _Optional[_Iterable[_Union[_struct_pb2.Struct, _Mapping]]] = ..., meta: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...
