from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ack(_message.Message):
    __slots__ = ("status", "message")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    status: str
    message: str
    def __init__(self, status: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class CreateRunRequest(_message.Message):
    __slots__ = ("run_id", "name", "project", "tags", "config_json", "created_at", "description", "notes", "entity")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    CONFIG_JSON_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    name: str
    project: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    config_json: str
    created_at: _timestamp_pb2.Timestamp
    description: str
    notes: str
    entity: str
    def __init__(self, run_id: _Optional[str] = ..., name: _Optional[str] = ..., project: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ..., config_json: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., description: _Optional[str] = ..., notes: _Optional[str] = ..., entity: _Optional[str] = ...) -> None: ...

class Record(_message.Message):
    __slots__ = ("timestamp", "payload_json", "payload_name", "sequence", "runtime")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_JSON_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_NAME_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    RUNTIME_FIELD_NUMBER: _ClassVar[int]
    timestamp: _timestamp_pb2.Timestamp
    payload_json: str
    payload_name: str
    sequence: int
    runtime: float
    def __init__(self, timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., payload_json: _Optional[str] = ..., payload_name: _Optional[str] = ..., sequence: _Optional[int] = ..., runtime: _Optional[float] = ...) -> None: ...

class StoreRecordBatchRequest(_message.Message):
    __slots__ = ("run_id", "project", "type", "records")
    RUN_ID_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    RECORDS_FIELD_NUMBER: _ClassVar[int]
    run_id: str
    project: str
    type: str
    records: _containers.RepeatedCompositeFieldContainer[Record]
    def __init__(self, run_id: _Optional[str] = ..., project: _Optional[str] = ..., type: _Optional[str] = ..., records: _Optional[_Iterable[_Union[Record, _Mapping]]] = ...) -> None: ...
