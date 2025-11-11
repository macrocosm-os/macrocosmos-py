from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetHotkeysResponse(_message.Message):
    __slots__ = ("hotkeys",)
    HOTKEYS_FIELD_NUMBER: _ClassVar[int]
    hotkeys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, hotkeys: _Optional[_Iterable[str]] = ...) -> None: ...

class BuyMarketplaceDatasetRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class BuyMarketplaceDatasetResponse(_message.Message):
    __slots__ = ("success", "message", "purchase_transaction_id")
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    purchase_transaction_id: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., purchase_transaction_id: _Optional[str] = ...) -> None: ...

class UserMarketplaceDataset(_message.Message):
    __slots__ = ("gravity_task_id", "created_at", "purchase_price_cents", "purchase_transaction_id")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_PRICE_CENTS_FIELD_NUMBER: _ClassVar[int]
    PURCHASE_TRANSACTION_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    created_at: _timestamp_pb2.Timestamp
    purchase_price_cents: int
    purchase_transaction_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., purchase_price_cents: _Optional[int] = ..., purchase_transaction_id: _Optional[str] = ...) -> None: ...

class GetUserMarketplaceDatasetsResponse(_message.Message):
    __slots__ = ("user_datasets",)
    USER_DATASETS_FIELD_NUMBER: _ClassVar[int]
    user_datasets: _containers.RepeatedCompositeFieldContainer[UserMarketplaceDataset]
    def __init__(self, user_datasets: _Optional[_Iterable[_Union[UserMarketplaceDataset, _Mapping]]] = ...) -> None: ...

class UpsertHotkeysRequest(_message.Message):
    __slots__ = ("hotkeys",)
    HOTKEYS_FIELD_NUMBER: _ClassVar[int]
    hotkeys: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, hotkeys: _Optional[_Iterable[str]] = ...) -> None: ...

class UpsertMarketplaceTaskSuggestionsRequest(_message.Message):
    __slots__ = ("gravity_task_id", "suggested_gravity_task_ids")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SUGGESTED_GRAVITY_TASK_IDS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    suggested_gravity_task_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, gravity_task_id: _Optional[str] = ..., suggested_gravity_task_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetMarketplaceTaskSuggestionsRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class GetMarketplaceTaskSuggestionsResponse(_message.Message):
    __slots__ = ("suggested_gravity_task_ids",)
    SUGGESTED_GRAVITY_TASK_IDS_FIELD_NUMBER: _ClassVar[int]
    suggested_gravity_task_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, suggested_gravity_task_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class PopularTag(_message.Message):
    __slots__ = ("tag", "count")
    TAG_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    tag: str
    count: int
    def __init__(self, tag: _Optional[str] = ..., count: _Optional[int] = ...) -> None: ...

class GetPopularTagsResponse(_message.Message):
    __slots__ = ("popular_tags",)
    POPULAR_TAGS_FIELD_NUMBER: _ClassVar[int]
    popular_tags: _containers.RepeatedCompositeFieldContainer[PopularTag]
    def __init__(self, popular_tags: _Optional[_Iterable[_Union[PopularTag, _Mapping]]] = ...) -> None: ...

class PublishDatasetRequest(_message.Message):
    __slots__ = ("dataset_id",)
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    def __init__(self, dataset_id: _Optional[str] = ...) -> None: ...

class PersistentDatasetWorkflow(_message.Message):
    __slots__ = ("dataset_id", "status")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    status: str
    def __init__(self, dataset_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

class AddPersistentDatasetWorkflowsRequest(_message.Message):
    __slots__ = ("dataset_workflows",)
    DATASET_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    dataset_workflows: _containers.RepeatedCompositeFieldContainer[PersistentDatasetWorkflow]
    def __init__(self, dataset_workflows: _Optional[_Iterable[_Union[PersistentDatasetWorkflow, _Mapping]]] = ...) -> None: ...

class UpsertMarketplaceTaskMetadataRequest(_message.Message):
    __slots__ = ("gravity_task_id", "description", "name", "image_url", "tags")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    description: str
    name: str
    image_url: str
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, gravity_task_id: _Optional[str] = ..., description: _Optional[str] = ..., name: _Optional[str] = ..., image_url: _Optional[str] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

class GetMarketplaceDatasetsRequest(_message.Message):
    __slots__ = ("popular",)
    POPULAR_FIELD_NUMBER: _ClassVar[int]
    popular: bool
    def __init__(self, popular: bool = ...) -> None: ...

class GetPersistentDatasetWorkflowsResponse(_message.Message):
    __slots__ = ("dataset_workflows",)
    DATASET_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    dataset_workflows: _containers.RepeatedCompositeFieldContainer[PersistentDatasetWorkflow]
    def __init__(self, dataset_workflows: _Optional[_Iterable[_Union[PersistentDatasetWorkflow, _Mapping]]] = ...) -> None: ...

class Crawler(_message.Message):
    __slots__ = ("crawler_id", "criteria", "start_time", "deregistration_time", "archive_time", "state", "dataset_workflows", "parquet_paths")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    CRITERIA_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DEREGISTRATION_TIME_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    DATASET_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    PARQUET_PATHS_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    criteria: CrawlerCriteria
    start_time: _timestamp_pb2.Timestamp
    deregistration_time: _timestamp_pb2.Timestamp
    archive_time: _timestamp_pb2.Timestamp
    state: CrawlerState
    dataset_workflows: _containers.RepeatedScalarFieldContainer[str]
    parquet_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, crawler_id: _Optional[str] = ..., criteria: _Optional[_Union[CrawlerCriteria, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., deregistration_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., archive_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., state: _Optional[_Union[CrawlerState, _Mapping]] = ..., dataset_workflows: _Optional[_Iterable[str]] = ..., parquet_paths: _Optional[_Iterable[str]] = ...) -> None: ...

class PersistentGravityTask(_message.Message):
    __slots__ = ("gravity_task_id", "ingest_dt")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    INGEST_DT_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    ingest_dt: str
    def __init__(self, gravity_task_id: _Optional[str] = ..., ingest_dt: _Optional[str] = ...) -> None: ...

class GetPersistentGravityTasksResponse(_message.Message):
    __slots__ = ("persistent_gravity_tasks",)
    PERSISTENT_GRAVITY_TASKS_FIELD_NUMBER: _ClassVar[int]
    persistent_gravity_tasks: _containers.RepeatedCompositeFieldContainer[PersistentGravityTask]
    def __init__(self, persistent_gravity_tasks: _Optional[_Iterable[_Union[PersistentGravityTask, _Mapping]]] = ...) -> None: ...

class UpsertCrawlerRequest(_message.Message):
    __slots__ = ("gravity_task_id", "crawler")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    crawler: Crawler
    def __init__(self, gravity_task_id: _Optional[str] = ..., crawler: _Optional[_Union[Crawler, _Mapping]] = ...) -> None: ...

class UpsertResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class UpsertGravityTaskRequest(_message.Message):
    __slots__ = ("gravity_task",)
    GRAVITY_TASK_FIELD_NUMBER: _ClassVar[int]
    gravity_task: GravityTaskRequest
    def __init__(self, gravity_task: _Optional[_Union[GravityTaskRequest, _Mapping]] = ...) -> None: ...

class UpsertGravityTaskResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...

class GravityTaskRequest(_message.Message):
    __slots__ = ("id", "name", "status", "start_time", "notification_to", "notification_link")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_TO_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_LINK_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    status: str
    start_time: _timestamp_pb2.Timestamp
    notification_to: str
    notification_link: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., notification_to: _Optional[str] = ..., notification_link: _Optional[str] = ...) -> None: ...

class InsertCrawlerCriteriaRequest(_message.Message):
    __slots__ = ("crawler_id", "crawler_criteria")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_CRITERIA_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    crawler_criteria: CrawlerCriteria
    def __init__(self, crawler_id: _Optional[str] = ..., crawler_criteria: _Optional[_Union[CrawlerCriteria, _Mapping]] = ...) -> None: ...

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

class PersistentTopic(_message.Message):
    __slots__ = ("platform", "topic")
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    platform: str
    topic: str
    def __init__(self, platform: _Optional[str] = ..., topic: _Optional[str] = ...) -> None: ...

class PersistentTopicResponse(_message.Message):
    __slots__ = ("persistent_topics",)
    PERSISTENT_TOPICS_FIELD_NUMBER: _ClassVar[int]
    persistent_topics: _containers.RepeatedCompositeFieldContainer[PersistentTopic]
    def __init__(self, persistent_topics: _Optional[_Iterable[_Union[PersistentTopic, _Mapping]]] = ...) -> None: ...

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

class GravityMarketplaceTaskState(_message.Message):
    __slots__ = ("gravity_task_id", "name", "status", "start_time", "crawler_ids", "crawler_workflows", "task_records_collected", "task_bytes_collected", "description", "image_url", "view_count", "download_count", "tags")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_IDS_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_WORKFLOWS_FIELD_NUMBER: _ClassVar[int]
    TASK_RECORDS_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    TASK_BYTES_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    IMAGE_URL_FIELD_NUMBER: _ClassVar[int]
    VIEW_COUNT_FIELD_NUMBER: _ClassVar[int]
    DOWNLOAD_COUNT_FIELD_NUMBER: _ClassVar[int]
    TAGS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    name: str
    status: str
    start_time: _timestamp_pb2.Timestamp
    crawler_ids: _containers.RepeatedScalarFieldContainer[str]
    crawler_workflows: _containers.RepeatedCompositeFieldContainer[Crawler]
    task_records_collected: int
    task_bytes_collected: int
    description: str
    image_url: str
    view_count: int
    download_count: int
    tags: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, gravity_task_id: _Optional[str] = ..., name: _Optional[str] = ..., status: _Optional[str] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., crawler_ids: _Optional[_Iterable[str]] = ..., crawler_workflows: _Optional[_Iterable[_Union[Crawler, _Mapping]]] = ..., task_records_collected: _Optional[int] = ..., task_bytes_collected: _Optional[int] = ..., description: _Optional[str] = ..., image_url: _Optional[str] = ..., view_count: _Optional[int] = ..., download_count: _Optional[int] = ..., tags: _Optional[_Iterable[str]] = ...) -> None: ...

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

class GetMarketplaceCrawlersResponse(_message.Message):
    __slots__ = ("crawler_id",)
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    crawler_id: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, crawler_id: _Optional[_Iterable[str]] = ...) -> None: ...

class CompleteCrawlerRequest(_message.Message):
    __slots__ = ("crawler_id", "status")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    status: str
    def __init__(self, crawler_id: _Optional[str] = ..., status: _Optional[str] = ...) -> None: ...

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
    __slots__ = ("crawler_id", "notification_requests", "max_rows", "is_marketplace")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    NOTIFICATION_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    MAX_ROWS_FIELD_NUMBER: _ClassVar[int]
    IS_MARKETPLACE_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    notification_requests: _containers.RepeatedCompositeFieldContainer[NotificationRequest]
    max_rows: int
    is_marketplace: bool
    def __init__(self, crawler_id: _Optional[str] = ..., notification_requests: _Optional[_Iterable[_Union[NotificationRequest, _Mapping]]] = ..., max_rows: _Optional[int] = ..., is_marketplace: bool = ...) -> None: ...

class BuildDatasetResponse(_message.Message):
    __slots__ = ("dataset_id", "dataset")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    dataset: Dataset
    def __init__(self, dataset_id: _Optional[str] = ..., dataset: _Optional[_Union[Dataset, _Mapping]] = ...) -> None: ...

class BuildAllDatasetsRequest(_message.Message):
    __slots__ = ("gravity_task_id", "build_crawlers_config", "is_marketplace")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    BUILD_CRAWLERS_CONFIG_FIELD_NUMBER: _ClassVar[int]
    IS_MARKETPLACE_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    build_crawlers_config: _containers.RepeatedCompositeFieldContainer[BuildDatasetRequest]
    is_marketplace: bool
    def __init__(self, gravity_task_id: _Optional[str] = ..., build_crawlers_config: _Optional[_Iterable[_Union[BuildDatasetRequest, _Mapping]]] = ..., is_marketplace: bool = ...) -> None: ...

class BuildAllDatasetsResponse(_message.Message):
    __slots__ = ("gravity_task_id", "datasets")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    datasets: _containers.RepeatedCompositeFieldContainer[Dataset]
    def __init__(self, gravity_task_id: _Optional[str] = ..., datasets: _Optional[_Iterable[_Union[Dataset, _Mapping]]] = ...) -> None: ...

class AddPersistentGravityTaskRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

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

class UpsertDatasetRequest(_message.Message):
    __slots__ = ("dataset_id", "dataset")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    dataset: Dataset
    def __init__(self, dataset_id: _Optional[str] = ..., dataset: _Optional[_Union[Dataset, _Mapping]] = ...) -> None: ...

class UpsertNebulaRequest(_message.Message):
    __slots__ = ("dataset_id", "nebula_id", "nebula")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    NEBULA_ID_FIELD_NUMBER: _ClassVar[int]
    NEBULA_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    nebula_id: str
    nebula: Nebula
    def __init__(self, dataset_id: _Optional[str] = ..., nebula_id: _Optional[str] = ..., nebula: _Optional[_Union[Nebula, _Mapping]] = ...) -> None: ...

class InsertDatasetFileRequest(_message.Message):
    __slots__ = ("dataset_id", "files")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    files: _containers.RepeatedCompositeFieldContainer[DatasetFile]
    def __init__(self, dataset_id: _Optional[str] = ..., files: _Optional[_Iterable[_Union[DatasetFile, _Mapping]]] = ...) -> None: ...

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

class GetMarketplaceDatasetsResponse(_message.Message):
    __slots__ = ("datasets",)
    DATASETS_FIELD_NUMBER: _ClassVar[int]
    datasets: _containers.RepeatedCompositeFieldContainer[GravityMarketplaceTaskState]
    def __init__(self, datasets: _Optional[_Iterable[_Union[GravityMarketplaceTaskState, _Mapping]]] = ...) -> None: ...

class GetGravityTaskDatasetFilesRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class CrawlerDatasetFiles(_message.Message):
    __slots__ = ("crawler_id", "dataset_files")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    DATASET_FILES_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    dataset_files: _containers.RepeatedCompositeFieldContainer[DatasetFileWithId]
    def __init__(self, crawler_id: _Optional[str] = ..., dataset_files: _Optional[_Iterable[_Union[DatasetFileWithId, _Mapping]]] = ...) -> None: ...

class CrawlerRawMinerFilesResponse(_message.Message):
    __slots__ = ("crawler_id", "s3_paths")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    S3_PATHS_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    s3_paths: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, crawler_id: _Optional[str] = ..., s3_paths: _Optional[_Iterable[str]] = ...) -> None: ...

class DatasetFileWithId(_message.Message):
    __slots__ = ("dataset_id", "file_name", "file_size_bytes", "last_modified", "num_rows", "s3_key", "url", "nebula_url")
    DATASET_ID_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    FILE_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    LAST_MODIFIED_FIELD_NUMBER: _ClassVar[int]
    NUM_ROWS_FIELD_NUMBER: _ClassVar[int]
    S3_KEY_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    NEBULA_URL_FIELD_NUMBER: _ClassVar[int]
    dataset_id: str
    file_name: str
    file_size_bytes: int
    last_modified: _timestamp_pb2.Timestamp
    num_rows: int
    s3_key: str
    url: str
    nebula_url: str
    def __init__(self, dataset_id: _Optional[str] = ..., file_name: _Optional[str] = ..., file_size_bytes: _Optional[int] = ..., last_modified: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., num_rows: _Optional[int] = ..., s3_key: _Optional[str] = ..., url: _Optional[str] = ..., nebula_url: _Optional[str] = ...) -> None: ...

class GetGravityTaskDatasetFilesResponse(_message.Message):
    __slots__ = ("gravity_task_id", "crawler_dataset_files")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_DATASET_FILES_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    crawler_dataset_files: _containers.RepeatedCompositeFieldContainer[CrawlerDatasetFiles]
    def __init__(self, gravity_task_id: _Optional[str] = ..., crawler_dataset_files: _Optional[_Iterable[_Union[CrawlerDatasetFiles, _Mapping]]] = ...) -> None: ...

class GetCrawlerHistoryRequest(_message.Message):
    __slots__ = ("gravity_task_id",)
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    def __init__(self, gravity_task_id: _Optional[str] = ...) -> None: ...

class CrawlerHistoryEntry(_message.Message):
    __slots__ = ("ingest_dt", "records_collected", "bytes_collected")
    INGEST_DT_FIELD_NUMBER: _ClassVar[int]
    RECORDS_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    BYTES_COLLECTED_FIELD_NUMBER: _ClassVar[int]
    ingest_dt: _timestamp_pb2.Timestamp
    records_collected: int
    bytes_collected: int
    def __init__(self, ingest_dt: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., records_collected: _Optional[int] = ..., bytes_collected: _Optional[int] = ...) -> None: ...

class CrawlerCriteriaAndHistory(_message.Message):
    __slots__ = ("crawler_id", "platform", "topic", "keyword", "post_start_date", "post_end_date", "crawler_history")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    POST_START_DATE_FIELD_NUMBER: _ClassVar[int]
    POST_END_DATE_FIELD_NUMBER: _ClassVar[int]
    CRAWLER_HISTORY_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    platform: str
    topic: str
    keyword: str
    post_start_date: _timestamp_pb2.Timestamp
    post_end_date: _timestamp_pb2.Timestamp
    crawler_history: _containers.RepeatedCompositeFieldContainer[CrawlerHistoryEntry]
    def __init__(self, crawler_id: _Optional[str] = ..., platform: _Optional[str] = ..., topic: _Optional[str] = ..., keyword: _Optional[str] = ..., post_start_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., post_end_date: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., crawler_history: _Optional[_Iterable[_Union[CrawlerHistoryEntry, _Mapping]]] = ...) -> None: ...

class GetCrawlerHistoryResponse(_message.Message):
    __slots__ = ("gravity_task_id", "crawlers")
    GRAVITY_TASK_ID_FIELD_NUMBER: _ClassVar[int]
    CRAWLERS_FIELD_NUMBER: _ClassVar[int]
    gravity_task_id: str
    crawlers: _containers.RepeatedCompositeFieldContainer[CrawlerCriteriaAndHistory]
    def __init__(self, gravity_task_id: _Optional[str] = ..., crawlers: _Optional[_Iterable[_Union[CrawlerCriteriaAndHistory, _Mapping]]] = ...) -> None: ...

class GetCrawlerDataForDDSubmissionRequest(_message.Message):
    __slots__ = ("dsns",)
    DSNS_FIELD_NUMBER: _ClassVar[int]
    dsns: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dsns: _Optional[_Iterable[str]] = ...) -> None: ...

class GetCrawlerDataForDDSubmissionResponse(_message.Message):
    __slots__ = ("crawlers",)
    CRAWLERS_FIELD_NUMBER: _ClassVar[int]
    crawlers: _containers.RepeatedCompositeFieldContainer[CrawlerDataForDD]
    def __init__(self, crawlers: _Optional[_Iterable[_Union[CrawlerDataForDD, _Mapping]]] = ...) -> None: ...

class CrawlerDataForDD(_message.Message):
    __slots__ = ("crawler_id", "platform", "topic", "keyword", "post_start_datetime", "post_end_datetime")
    CRAWLER_ID_FIELD_NUMBER: _ClassVar[int]
    PLATFORM_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    KEYWORD_FIELD_NUMBER: _ClassVar[int]
    POST_START_DATETIME_FIELD_NUMBER: _ClassVar[int]
    POST_END_DATETIME_FIELD_NUMBER: _ClassVar[int]
    crawler_id: str
    platform: str
    topic: str
    keyword: str
    post_start_datetime: str
    post_end_datetime: str
    def __init__(self, crawler_id: _Optional[str] = ..., platform: _Optional[str] = ..., topic: _Optional[str] = ..., keyword: _Optional[str] = ..., post_start_datetime: _Optional[str] = ..., post_end_datetime: _Optional[str] = ...) -> None: ...
