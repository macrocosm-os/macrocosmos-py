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
