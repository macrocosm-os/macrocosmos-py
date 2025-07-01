# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class Ack(BaseModel):
    """
     Ack is a response to a request
    """

# status is the status of the request
    status: str = Field(default="")
# message is the message of the request
    message: str = Field(default="")

class CreateRunRequest(BaseModel):
    """
     CreateRunRequest is a request to create a new run
    """

# run_id is the ID of the run
    run_id: str = Field(default="")
# name is the name of the run
    name: str = Field(default="")
# project is the project of the run
    project: str = Field(default="")
# tags are the tags of the run
    tags: typing.List[str] = Field(default_factory=list)
# config_json is the config of the run
    config_json: str = Field(default="")
# created_at is the timestamp of the run
    created_at: datetime = Field(default_factory=datetime.now)
# description is the description of the run
    description: typing.Optional[str] = Field(default="")
# notes are the notes of the run
    notes: typing.Optional[str] = Field(default="")
# entity is the entity of the run
    entity: typing.Optional[str] = Field(default="")

class Record(BaseModel):
    """
     Record is a record in the logger
    """

# timestamp is the timestamp of the record
    timestamp: datetime = Field(default_factory=datetime.now)
# payload_json is the payload of the record
    payload_json: str = Field(default="")
# payload_name is the name of the payload (used in artifact storage)
    payload_name: typing.Optional[str] = Field(default="")
# sequence is the sequence of the record (used as "step" in history)
    sequence: typing.Optional[int] = Field(default=0)
# runtime is the runtime of the record (seconds since ran began)
    runtime: typing.Optional[float] = Field(default=0.0)

class StoreRecordBatchRequest(BaseModel):
    """
     StoreRecordBatchRequest is a request to store a batch of records
    """

# run_id is the ID of the run
    run_id: str = Field(default="")
# project is the project of the record
    project: str = Field(default="")
# type is the record type
    type: str = Field(default="")
# records are the records to store
    records: typing.List[Record] = Field(default_factory=list)
