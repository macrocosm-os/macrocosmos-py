from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Crawler(_message.Message):
    __slots__ = ("crawler_id", "criteria", "start_time", "deregistration_time", "archive_time", "state", "dataset_workflows")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DEREGISTRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    DATASET_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    criteria: CrawlerCriteria
    start_time: _timestamp_pb2.Timestamp
    deregistration_time: _timestamp_pb2.Timestamp
    archive_time: _timestamp_pb2.Timestamp
    state: CrawlerState
    dataset_workflows: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, crawler_id: _Optional[str] = ..., criteria: _Optional[_Union[CrawlerCriteria, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., deregistration_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., archive_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[CrawlerState, _Mapping]] = ..., dataset_workflows: _Optional[_Iterable[str]] = ...) -> None: ...

class CrawlerCriteria(_message.Message):
    __slots__ = ("platform", "topic", "notification", "mock", "user_id", "keyword", "post_start_datetime", "post_end_datetime")
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_FIELD_NUMBER: _ClassVar[int]
    MOCK_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    POST_START_DATETIME_FIELD_NUMBER: _ClassVar[int]
    POST_END_DATETIME_FIELD_NUMBER: _ClassVar[int]
    platform: str
    topic: str
    notification: CrawlerNotification
    mock: bool
    user_id: str
    keyword: str
    post_start_datetime: _timestamp_pb2.Timestamp
    post_end_datetime: _timestamp_pb2.Timestamp
    def __init__(self, platform: _Optional[str] = ..., topic: _Optional[str] = ..., notification: _Optional[_Union[CrawlerNotification, _Mapping]] = ..., mock: bool = ..., user_id: _Optional[str] = ..., keyword: _Optional[str] = ..., post_start_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., post_end_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CrawlerNotification(_message.Message):
    __slots__ = ("to", "link")
    TO_FIELD_NUMBER: _ClassVar[int]
    LINK_FIELD_NUMBER: _ClassVar[int]
    to: str
    link: str
    def __init__(self, to: _Optional[str] = ..., link: _Optional[str] = ...) -> None: ...

class HfRepo(_message.Message):
    __slots__ = ("repo_name", "row_count", "last_update")
    REPO_NAME_FIELD_NUMBER: _ClassVar[int]
    ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    LAST_UPDATE_FIELD_NUMBER: _ClassVar[int]
    repo_name: str
    row_count: int
    last_update: str
    def __init__(self, repo_name: _Optional[str] = ..., row_count: _Optional[int] = ..., last_update: _Optional[str] = ...) -> None: ...

class CrawlerState(_message.Message):
    __slots__ = ("status", "bytes_collected", "records_collected", "repos")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    RECORDS_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    REPOS_FIELD_NUMBER: _ClassVar[int]
    status: str
    bytes_collected: int
    records_collected: int
    repos: _containers.RepeatedCompositeFieldContainer[HfRepo]
    def __init__(self, status: _Optional[str] = ..., bytes_collected: _Optional[int] = ..., records_collected: _Optional[int] = ..., repos: _Optional[_Iterable[_Union[HfRepo, _Mapping]]] = ...) -> None: ...

class GravityTaskState(_message.Message):
    __slots__ = ("gravity_task_id", "name", "status", "start_time", "crawler_ids", "crawler_workflows")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_IDS_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    name: str
    status: str
    start_time: _timestamp_pb2.Timestamp
    crawler_ids: _containers.RepeatedScalarFieldContainer[str]
    crawler_workflows: _containers.RepeatedCompositeFieldContainer[Crawler]
    def __init__(self, gravity_task_id: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., crawler_ids: _Optional[_Iterable[str]] = ..., crawler_workflows: _Optional[_Iterable[_Union[Crawler, _Mapping]]] = ...) -> None: ...

class GetGravityTasksRequest(_message.Message):
    __slots__ = ("gravity_task_id", "include_crawlers")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    INCLUDE_CRAWLERS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    include_crawlers: bool
    def __init__(self, gravity_task_id: _Optional[str] = ..., include_crawlers: bool = ...) -> None: ...

class GetGravityTasksResponse(_message.Message):
    __slots__ = ("gravity_task_states",)
    GRAVITY_TASK_STATES_FIELD_NUMBER: _ClassVar[int]
    gravity_task_states: _containers.RepeatedCompositeFieldContainer[GravityTaskState]
    def __init__(self, gravity_task_states: _Optional[_Iterable[_Union[GravityTaskState, _Mapping]]] = ...) -> None: ...

class GravityTask(_message.Message):
    __slots__ = ("topic", "platform", "keyword", "post_start_datetime", "post_end_datetime")
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    POST_START_DATETIME_FIELD_NUMBER: _ClassVar[int]
    POST_END_DATETIME_FIELD_NUMBER: _ClassVar[int]
    topic: str
    platform: str
    keyword: str
    post_start_datetime: _timestamp_pb2.Timestamp
    post_end_datetime: _timestamp_pb2.Timestamp
    def __init__(self, topic: _Optional[str] = ..., platform: _Optional[str] = ..., keyword: _Optional[str] = ..., post_start_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., post_end_datetime: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class NotificationRequest(_message.Message):
    __slots__ = ("type", "address", "redirect_url")
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    REDIRECT_URL_FIELD_NUMBER: _ClassVar[int]
    type: str
    address: str
    redirect_url: str
    def __init__(self, type: _Optional[str] = ..., address: _Optional[str] = ..., redirect_url: _Optional[str] = ...) -> None: ...

class GetCrawlerRequest(_message.Message):
    __slots__ = ("crawler_id",)
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    def __init__(self, crawler_id: _Optional[str] = ...) -> None: ...

class GetCrawlerResponse(_message.Message):
    __slots__ = ("crawler",)
    CRAWLER_FIELD_NUMBER: _ClassVar[int]
    crawler: Crawler
    def __init__(self, crawler: _Optional[_Union[Crawler, _Mapping]] = ...) -> None: ...

class CreateGravityTaskRequest(_message.Message):
    __slots__ = ("gravity_tasks", "name", "notification_requests", "gravity_task_id")
    GRAVITY_TASKS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_tasks: _containers.RepeatedCompositeFieldContainer[GravityTask]
    name: str
    notification_requests: _containers.RepeatedCompositeFieldContainer[NotificationRequest]
    gravity_task_id: str
    def __init__(self, gravity_tasks: _Optional[_Iterable[_Union[GravityTask, _Mapping]]] = ..., name: _Optional[str] = ..., notification_requests: _Optional[_Iterable[_Union[NotificationRequest, _Mapping]]] = ..., gravity_task_id: _Optional[str] = ...) -> None: ...

class CreateGravityTaskResponse(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class BuildDatasetRequest(_message.Message):
    __slots__ = ("crawler_id", "notification_requests", "max_rows")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    MAX_ROWS_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    notification_requests: _containers.RepeatedCompositeFieldContainer[NotificationRequest]
    max_rows: int
    def __init__(self, crawler_id: _Optional[str] = ..., notification_requests: _Optional[_Iterable[_Union[NotificationRequest, _Mapping]]] = ..., max_rows: _Optional[int] = ...) -> None: ...

class BuildDatasetResponse(_message.Message):
    __slots__ = ("dataset_id", "dataset")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    dataset: Dataset
    def __init__(self, dataset_id: _Optional[str] = ..., dataset: _Optional[_Union[Dataset, _Mapping]] = ...) -> None: ...

class Nebula(_message.Message):
    __slots__ = ("error", "file_size_bytes", "url")
    ERROR_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    error: str
    file_size_bytes: int
    url: str
    def __init__(self, error: _Optional[str] = ..., file_size_bytes: _Optional[int] = ..., url: _Optional[str] = ...) -> None: ...

class Dataset(_message.Message):
    __slots__ = ("crawler_workflow_id", "create_date", "expire_date", "files", "status", "status_message", "steps", "total_steps", "nebula")
    CRAWLER_WORKFLOW_ID_FIELD_NUMBER: _ClassVar[int]
    CREATE_DATE_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_DATE_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_STEPS_FIELD_NUMBER: _ClassVar[int]
    NEBULA_FIELD_NUMBER: _ClassVar[int]
    crawler_workflow_id: str
    create_date: _timestamp_pb2.Timestamp
    expire_date: _timestamp_pb2.Timestamp
    files: _containers.RepeatedCompositeFieldContainer[DatasetFile]
    status: str
    status_message: str
    steps: _containers.RepeatedCompositeFieldContainer[DatasetStep]
    total_steps: int
    nebula: Nebula
    def __init__(self, crawler_workflow_id: _Optional[str] = ..., create_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., expire_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., files: _Optional[_Iterable[_Union[DatasetFile, _Mapping]]] = ..., status: _Optional[str] = ..., status_message: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[DatasetStep, _Mapping]]] = ..., total_steps: _Optional[int] = ..., nebula: _Optional[_Union[Nebula, _Mapping]] = ...) -> None: ...

class DatasetFile(_message.Message):
    __slots__ = ("file_name", "file_size_bytes", "last_modified", "num_rows", "s3_key", "url")
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    S3_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    file_name: str
    file_size_bytes: int
    last_modified: _timestamp_pb2.Timestamp
    num_rows: int
    s3_key: str
    url: str
    def __init__(self, file_name: _Optional[str] = ..., file_size_bytes: _Optional[int] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., num_rows: _Optional[int] = ..., s3_key: _Optional[str] = ..., url: _Optional[str] = ...) -> None: ...

class DatasetStep(_message.Message):
    __slots__ = ("progress", "step", "step_name")
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    STEP_NAME_FIELD_NUMBER: _ClassVar[int]
    progress: float
    step: int
    step_name: str
    def __init__(self, progress: _Optional[float] = ..., step: _Optional[int] = ..., step_name: _Optional[str] = ...) -> None: ...

class GetDatasetRequest(_message.Message):
    __slots__ = ("dataset_id",)
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    def __init__(self, dataset_id: _Optional[str] = ...) -> None: ...

class GetDatasetResponse(_message.Message):
    __slots__ = ("dataset",)
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset: Dataset
    def __init__(self, dataset: _Optional[_Union[Dataset, _Mapping]] = ...) -> None: ...

class CancelGravityTaskRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class CancelGravityTaskResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class CancelDatasetRequest(_message.Message):
    __slots__ = ("dataset_id",)
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    def __init__(self, dataset_id: _Optional[str] = ...) -> None: ...

class CancelDatasetResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class DatasetBillingCorrectionRequest(_message.Message):
    __slots__ = ("requested_row_count", "actual_row_count")
    REQUESTED_ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    ACTUAL_ROW_COUNT_FIELD_NUMBER: _ClassVar[int]
    requested_row_count: int
    actual_row_count: int
    def __init__(self, requested_row_count: _Optional[int] = ..., actual_row_count: _Optional[int] = ...) -> None: ...

class DatasetBillingCorrectionResponse(_message.Message):
    __slots__ = ("refund_amount",)
    REFUND_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    refund_amount: float
    def __init__(self, refund_amount: _Optional[float] = ...) -> None: ...
