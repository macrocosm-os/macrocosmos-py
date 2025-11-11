# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class GetHotkeysResponse(BaseModel):
    """
     GetHotkeysResponse is the response message for getting hotkeys
    """

# hotkeys: the hotkeys
    hotkeys: typing.List[str] = Field(default_factory=list)

class BuyMarketplaceDatasetRequest(BaseModel):
    """
     BuyMarketplaceDatasetRequest is the request to purchase a dataset
    """

# gravity_task_id: the marketplace dataset's gravity task id to purchase
    gravity_task_id: str = Field(default="")

class BuyMarketplaceDatasetResponse(BaseModel):
    """
     BuyMarketplaceDatasetResponse is the response to a dataset purchase
    """

# success: whether the purchase succeeded
    success: bool = Field(default=False)
# message: optional detail
    message: str = Field(default="")
# purchase_transaction_id: billing transaction id
    purchase_transaction_id: str = Field(default="")

class UserMarketplaceDataset(BaseModel):
    """
     UserMarketplaceDataset represents a single owned dataset record
    """

    gravity_task_id: str = Field(default="")
    created_at: datetime = Field(default_factory=datetime.now)
    purchase_price_cents: int = Field(default=0)
    purchase_transaction_id: str = Field(default="")

class GetUserMarketplaceDatasetsResponse(BaseModel):
    """
     GetUserMarketplaceDatasetsResponse lists owned datasets
    """

    user_datasets: typing.List[UserMarketplaceDataset] = Field(default_factory=list)

class UpsertHotkeysRequest(BaseModel):
    """
     UpsertHotkeysRequest is the request message for upserting hotkeys
    """

# hotkeys: the hotkeys to upsert
    hotkeys: typing.List[str] = Field(default_factory=list)

class UpsertMarketplaceTaskSuggestionsRequest(BaseModel):
    """
     UpsertMarketplaceTaskSuggestionsRequest is the request message for upserting marketplace task suggestions
    """

# gravity_task_id: the id of the gravity task
    gravity_task_id: str = Field(default="")
# suggested_gravity_task_ids: the ids of the suggested gravity tasks
    suggested_gravity_task_ids: typing.List[str] = Field(default_factory=list)

class GetMarketplaceTaskSuggestionsRequest(BaseModel):
    """
     GetMarketplaceTaskSuggestionsRequest is the request message for getting marketplace task suggestions
    """

# gravity_task_id: the id of the gravity task
    gravity_task_id: str = Field(default="")

class GetMarketplaceTaskSuggestionsResponse(BaseModel):
    """
     GetMarketplaceTaskSuggestionsResponse is the response message for getting marketplace task suggestions
    """

# suggested_gravity_task_ids: the ids of the suggested gravity tasks
    suggested_gravity_task_ids: typing.List[str] = Field(default_factory=list)

class PopularTag(BaseModel):
    """
     PopularTag is a single popular tag along with its count
    """

# tag: the popular tag
    tag: str = Field(default="")
# count: the count of the tag
    count: int = Field(default=0)

class GetPopularTagsResponse(BaseModel):
    """
     GetPopularTagsResponse is the response message for getting popular tags
    """

# popular_tags: the popular tags
    popular_tags: typing.List[PopularTag] = Field(default_factory=list)

class PublishDatasetRequest(BaseModel):
    """
     PublishDatasetRequest is the request message for publishing a dataset
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")

class PersistentDatasetWorkflow(BaseModel):
    """
     PersistentDatasetWorkflow
    """

# dataset_id: the ID of the dataset workflow
    dataset_id: str = Field(default="")
# status: the status of the dataset workflow
    status: str = Field(default="")

class AddPersistentDatasetWorkflowsRequest(BaseModel):
    """
     AddPersistentDatasetWorkflowsRequest
    """

    dataset_workflows: typing.List[PersistentDatasetWorkflow] = Field(default_factory=list)

class UpsertMarketplaceTaskMetadataRequest(BaseModel):
    """
     UpsertMarketplaceTaskMetadataRequest
    """

# gravity_task_id: the id of the gravity task 
    gravity_task_id: str = Field(default="")
# description: a description of the curated gravity task 
    description: str = Field(default="")
# name: the name of the curated task 
    name: str = Field(default="")
# image_url: points to an image related to the task
    image_url: str = Field(default="")
# tags: a set of tags for this task 
    tags: typing.List[str] = Field(default_factory=list)

class GetMarketplaceDatasetsRequest(BaseModel):
    """
     GetMarketplaceDatasetsRequest is the request message for getting marketplace datasets
    """

# popular: whether to return popular datasets
    popular: bool = Field(default=False)

class GetPersistentDatasetWorkflowsResponse(BaseModel):
    """
     GetPersistentDatasetWorkflowsResponse returns recent dataset workflows
    """

    dataset_workflows: typing.List[PersistentDatasetWorkflow] = Field(default_factory=list)

class CrawlerNotification(BaseModel):
    """
     CrawlerNotification is the details of the notification to be sent to the user
    """

# to: the email address of the user
    to: str = Field(default="")
# link: the redirect link in the email where the user can view the dataset
    link: str = Field(default="")

class CrawlerCriteria(BaseModel):
    """
     CrawlerCriteria is the contents of the job and the notification details
    """

# platform: the platform of the job ('x' or 'reddit')
    platform: str = Field(default="")
# topic: the topic of the job (e.g. '#ai' for X, 'r/ai' for Reddit)
    topic: typing.Optional[str] = Field(default="")
# notification: the details of the notification to be sent to the user
    notification: CrawlerNotification = Field(default_factory=CrawlerNotification)
# mock: Used for testing purposes (optional, defaults to false)
    mock: bool = Field(default=False)
# user_id: the ID of the user who created the gravity task
    user_id: str = Field(default="")
# keyword: the keyword to search for in the job (optional)
    keyword: typing.Optional[str] = Field(default="")
# post_start_datetime: the start date of the job (optional)
    post_start_datetime: typing.Optional[datetime] = Field(default_factory=datetime.now)
# post_end_datetime: the end date of the job (optional)
    post_end_datetime: typing.Optional[datetime] = Field(default_factory=datetime.now)

class HfRepo(BaseModel):
    """
     HfRepo is a single Hugging Face repository that contains data for a crawler
    """

# repo_name: the name of the Hugging Face repository
    repo_name: str = Field(default="")
# row_count: the number of rows in the repository for the crawler criteria
    row_count: int = Field(default=0)
# last_update: the last recorded time the repository was updated
    last_update: str = Field(default="")

class CrawlerState(BaseModel):
    """
     CrawlerState is the current state of the crawler
    """

# status: the current status of the crawler
#   "Pending"   -- Crawler is pending submission to the SN13 Validator
#   "Submitted" -- Crawler is submitted to the SN13 Validator
#   "Running"   -- Crawler is running (we got the first update)
#   "Completed" -- Crawler is completed (timer expired)
#   "Cancelled" -- Crawler is cancelled by user via cancellation of workflow
#   "Archived"  -- Crawler is archived (now read-only i.e. no new dataset)
#   "Failed"    -- Crawler failed to run
    status: str = Field(default="")
# bytes_collected: the estimated number of bytes collected by the crawler
    bytes_collected: int = Field(default=0)
# records_collected: the estimated number of records collected by the crawler
    records_collected: int = Field(default=0)
# repos: the Hugging Face repositories that contain data for a crawler
    repos: typing.List[HfRepo] = Field(default_factory=list)

class Crawler(BaseModel):
    """
     Crawler is a single crawler workflow that registers a single job
 (platform/topic) on SN13's dynamic desirability engine
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")
# criteria: the contents of the job and the notification details
    criteria: CrawlerCriteria = Field(default_factory=CrawlerCriteria)
# start_time: the time the crawler was created
    start_time: datetime = Field(default_factory=datetime.now)
# deregistration_time: the time the crawler was deregistered
    deregistration_time: datetime = Field(default_factory=datetime.now)
# archive_time: the time the crawler was archived
    archive_time: datetime = Field(default_factory=datetime.now)
# state: the current state of the crawler
    state: CrawlerState = Field(default_factory=CrawlerState)
# dataset_workflows: the IDs of the dataset workflows that are associated
# with the crawler
    dataset_workflows: typing.List[str] = Field(default_factory=list)
# parquet_paths: the paths to the raw miner files collected
    parquet_paths: typing.List[str] = Field(default_factory=list)

class PersistentGravityTask(BaseModel):
    """
     PersistentGravityTask: a single persistent gravity task
    """

# gravity_task_id: the id of the gravity task
    gravity_task_id: str = Field(default="")
# ingest_dt: the date the task was ingested
    ingest_dt: str = Field(default="")

class GetPersistentGravityTasksResponse(BaseModel):
    """
     GetPersistentGravityTasksResponse: message containing persistent task ids and
 their ingest dt
    """

# persistent_gravity_tasks: the persistent gravity tasks
    persistent_gravity_tasks: typing.List[PersistentGravityTask] = Field(default_factory=list)

class UpsertCrawlerRequest(BaseModel):
    """
     UpsertCrawlerRequest for upserting a crawler and its criteria
    """

# gravity_task_id: the parent workflow id -- in this case the multicrawler id
    gravity_task_id: str = Field(default="")
# crawler: the crawler to upsert into the database
    crawler: Crawler = Field(default_factory=Crawler)

class UpsertResponse(BaseModel):
    """
     UpsertResponse is the response message for upserting a crawler
    """

# message: the message of upserting a crawler (currently hardcoded to
# "success")
    message: str = Field(default="")

class GravityTaskRequest(BaseModel):
    """
     GravityTaskRequest represents the data needed to upsert a gravity task
    """

# id: the ID of the gravity task
    id: str = Field(default="")
# name: the name of the gravity task
    name: str = Field(default="")
# status: the status of the gravity task
    status: str = Field(default="")
# start_time: the start time of the gravity task
    start_time: datetime = Field(default_factory=datetime.now)
# notification_to: the notification email address
    notification_to: str = Field(default="")
# notification_link: the notification redirect link
    notification_link: str = Field(default="")

class UpsertGravityTaskRequest(BaseModel):
    """
     UpsertGravityTaskRequest for upserting a gravity task
    """

# gravity_task: the gravity task to upsert into the database
    gravity_task: GravityTaskRequest = Field(default_factory=GravityTaskRequest)

class UpsertGravityTaskResponse(BaseModel):
    """
     UpsertGravityTaskResponse is the response message for upserting a gravity
 task
    """

# message: the message of upserting a gravity task (currently hardcoded to
# "success")
    message: str = Field(default="")

class InsertCrawlerCriteriaRequest(BaseModel):
    """
     UpsertCrawlerCriteriaRequest for upserting a crawler and its criteria
    """

# crawler_id: the id of the crawler
    crawler_id: str = Field(default="")
# crawler_criteria: the crawler criteria to upsert into the database
    crawler_criteria: CrawlerCriteria = Field(default_factory=CrawlerCriteria)

class PersistentTopic(BaseModel):
    """
     PersistentTopic is the contents of the persistent topic
    """

# platform: the platform of the job ('x' or 'reddit')
    platform: str = Field(default="")
# topic: the topic of the job (e.g. '#ai' for X, 'r/ai' for Reddit)
    topic: typing.Optional[str] = Field(default="")

class PersistentTopicResponse(BaseModel):
# persistent_topics: the persistent topics
    persistent_topics: typing.List[PersistentTopic] = Field(default_factory=list)

class GravityTaskState(BaseModel):
    """
     GravityTaskState is the current state of a gravity task
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")
# name: the name given by the user of the gravity task
    name: str = Field(default="")
# status: the current status of the gravity task
    status: str = Field(default="")
# start_time: the time the gravity task was created
    start_time: datetime = Field(default_factory=datetime.now)
# crawler_ids: the IDs of the crawler workflows that are associated with the
# gravity task
    crawler_ids: typing.List[str] = Field(default_factory=list)
# crawler_workflows: the crawler workflows that are associated with the
# gravity task
    crawler_workflows: typing.List[Crawler] = Field(default_factory=list)

class GravityMarketplaceTaskState(BaseModel):
    """
     GravityMarketplaceTaskState is the current state of a gravity task for marketplace display
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")
# name: the name given by the user of the gravity task
    name: str = Field(default="")
# status: the current status of the gravity task
    status: str = Field(default="")
# start_time: the time the gravity task was created
    start_time: datetime = Field(default_factory=datetime.now)
# crawler_ids: the IDs of the crawler workflows that are associated with the
# gravity task
    crawler_ids: typing.List[str] = Field(default_factory=list)
# crawler_workflows: the crawler workflows that are associated with the
# gravity task
    crawler_workflows: typing.List[Crawler] = Field(default_factory=list)
# task_records_collected: the total number of records collected across all crawlers for this task
    task_records_collected: int = Field(default=0)
# task_bytes_collected: the total number of bytes collected across all crawlers for this task
    task_bytes_collected: int = Field(default=0)
# description: description from gravity_marketplace_task_metadata
    description: str = Field(default="")
# image_url: image url from gravity_marketplace_task_metadata
    image_url: str = Field(default="")
# view_count: number of views from gravity_marketplace_task_download_history
    view_count: int = Field(default=0)
# download_count: number of downloads from gravity_marketplace_task_download_history
    download_count: int = Field(default=0)
# tags: set of tags from gravity_marketplace_task_tags (accumulated)
    tags: typing.List[str] = Field(default_factory=list)

class GetGravityTasksRequest(BaseModel):
    """
     GetGravityTasksRequest is the request message for listing gravity tasks for a
 user
    """

# gravity_task_id: the ID of the gravity task (optional, if not provided, all
# gravity tasks for the user will be returned)
    gravity_task_id: typing.Optional[str] = Field(default="")
# include_crawlers: whether to include the crawler states in the response
    include_crawlers: typing.Optional[bool] = Field(default=False)

class GetGravityTasksResponse(BaseModel):
    """
     GetGravityTasksResponse is the response message for listing gravity tasks for
 a user
    """

# gravity_task_states: the current states of the gravity tasks
    gravity_task_states: typing.List[GravityTaskState] = Field(default_factory=list)

class GravityTask(BaseModel):
    """
     GravityTask defines a crawler's criteria for a single job (platform/topic)
    """

# topic: the topic of the job (e.g. '#ai' for X, 'r/ai' for Reddit)
    topic: typing.Optional[str] = Field(default="")
# platform: the platform of the job ('x' or 'reddit')
    platform: str = Field(default="")
# keyword: the keyword to search for in the job (optional)
    keyword: typing.Optional[str] = Field(default="")
# post_start_datetime: the start date of the job (optional)
    post_start_datetime: typing.Optional[datetime] = Field(default_factory=datetime.now)
# post_end_datetime: the end date of the job (optional)
    post_end_datetime: typing.Optional[datetime] = Field(default_factory=datetime.now)

class NotificationRequest(BaseModel):
    """
     NotificationRequest is the request message for sending a notification to a
 user when a dataset is ready to download
    """

# type: the type of notification to send ('email' is only supported
# currently)
    type: str = Field(default="")
# address: the address to send the notification to (only email addresses are
# supported currently)
    address: str = Field(default="")
# redirect_url: the URL to include in the notication message that redirects
# the user to any built datasets
    redirect_url: typing.Optional[str] = Field(default="")

class GetCrawlerRequest(BaseModel):
    """
     GetCrawlerRequest is the request message for getting a crawler
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")

class GetMarketplaceCrawlersResponse(BaseModel):
    """
     GetMarketplaceCrawlersResponse is the response message holding all marketplace crawlers
    """

# crawler_id: the ID of the crawler
    crawler_id: typing.List[str] = Field(default_factory=list)

class CompleteCrawlerRequest(BaseModel):
    """
     CompleteCrawlerRequest is the request message for cancelling a crawler
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")
# status: ending status of the crawler
    status: str = Field(default="")

class GetCrawlerResponse(BaseModel):
    """
     GetCrawlerResponse is the response message for getting a crawler
    """

# crawler: the crawler
    crawler: Crawler = Field(default_factory=Crawler)

class CreateGravityTaskRequest(BaseModel):
    """
     CreateGravityTaskRequest is the request message for creating a new gravity
 task
    """

# gravity_tasks: the criteria for the crawlers that will be created
    gravity_tasks: typing.List[GravityTask] = Field(default_factory=list)
# name: the name of the gravity task (optional, default will generate a
# random name)
    name: str = Field(default="")
# notification_requests: the details of the notification to be sent to the
# user when a dataset
#   that is automatically generated upon completion of the crawler is ready
#   to download (optional)
    notification_requests: typing.List[NotificationRequest] = Field(default_factory=list)
# gravity_task_id: the ID of the gravity task (optional, default will
# generate a random ID)
    gravity_task_id: typing.Optional[str] = Field(default="")

class CreateGravityTaskResponse(BaseModel):
    """
     CreateGravityTaskResponse is the response message for creating a new gravity
 task
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")

class BuildDatasetRequest(BaseModel):
    """
     BuildDatasetRequest is the request message for manually requesting the
 building of a dataset for a single crawler
    """

# crawler_id: the ID of the crawler that will be used to build the dataset
    crawler_id: str = Field(default="")
# notification_requests: the details of the notification to be sent to the
# user when the dataset is ready to download (optional)
    notification_requests: typing.List[NotificationRequest] = Field(default_factory=list)
# max_rows: the maximum number of rows to include in the dataset (optional,
# defaults to 500)
    max_rows: int = Field(default=0)
# is_marketplace: determines whether the dataset to build is for marketplace 
    is_marketplace: typing.Optional[bool] = Field(default=False)

class DatasetFile(BaseModel):
    """
     DatasetFile contains the details about a dataset file
    """

# file_name: the name of the file
    file_name: str = Field(default="")
# file_size_bytes: the size of the file in bytes
    file_size_bytes: int = Field(default=0)
# last_modified: the date the file was last modified
    last_modified: datetime = Field(default_factory=datetime.now)
# num_rows: the number of rows in the file
    num_rows: int = Field(default=0)
# s3_key: the key of the file in S3 (internal use only)
    s3_key: str = Field(default="")
# url: the URL of the file (public use)
    url: str = Field(default="")

class DatasetStep(BaseModel):
    """
     DatasetStep contains one step of the progress of a dataset build
 (NOTE: each step varies in time and complexity)
    """

# progress: the progress of this step in the dataset build (0.0 - 1.0)
    progress: float = Field(default=0.0)
# step: the step number of the dataset build (1-indexed)
    step: int = Field(default=0)
# step_name: description of what is happening in the step
    step_name: str = Field(default="")

class Nebula(BaseModel):
# error: nebula build error message
    error: str = Field(default="")
# file_size_bytes: the size of the file in bytes
    file_size_bytes: int = Field(default=0)
# url: the URL of the file
    url: str = Field(default="")

class Dataset(BaseModel):
    """
     Dataset contains the progress and results of a dataset build
    """

# crawler_workflow_id: the ID of the parent crawler for this dataset
    crawler_workflow_id: str = Field(default="")
# create_date: the date the dataset was created
    create_date: datetime = Field(default_factory=datetime.now)
# expire_date: the date the dataset will expire (be deleted)
    expire_date: datetime = Field(default_factory=datetime.now)
# files: the details about the dataset files that are included in the dataset
    files: typing.List[DatasetFile] = Field(default_factory=list)
# status: the status of the dataset
    status: str = Field(default="")
# status_message: the message of the status of the dataset
    status_message: str = Field(default="")
# steps: the progress of the dataset build
    steps: typing.List[DatasetStep] = Field(default_factory=list)
# total_steps: the total number of steps in the dataset build
    total_steps: int = Field(default=0)
# nebula: the details about the nebula that was built
    nebula: Nebula = Field(default_factory=Nebula)

class BuildDatasetResponse(BaseModel):
    """
     BuildDatasetResponse is the response message for manually requesting the
 building of a dataset for a single crawler
 - dataset: the dataset that was built
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")
# dataset: the dataset that was built
    dataset: Dataset = Field(default_factory=Dataset)

class BuildAllDatasetsRequest(BaseModel):
    """
     BuildAllDatasetsRequest is the request message for building all datasets
 belonging to a workflow
    """

# gravityTaskId specifies which task to build
    gravity_task_id: str = Field(default="")
# specifies how much of each crawler to build for workflow
    build_crawlers_config: typing.List[BuildDatasetRequest] = Field(default_factory=list)
# is_marketplace: determines whether the datasets to build are for marketplace 
    is_marketplace: typing.Optional[bool] = Field(default=False)

class BuildAllDatasetsResponse(BaseModel):
    gravity_task_id: str = Field(default="")
    datasets: typing.List[Dataset] = Field(default_factory=list)

class AddPersistentGravityTaskRequest(BaseModel):
# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")

class UpsertDatasetRequest(BaseModel):
    """
     UpsertDatasetRequest contains the dataset id to insert and the dataset
 details
    """

# dataset_id: a unique id for the dataset
    dataset_id: str = Field(default="")
# dataset: the details of the dataset
    dataset: Dataset = Field(default_factory=Dataset)

class UpsertNebulaRequest(BaseModel):
    """
     UpsertNebulaRequest contains the dataset id and nebula details to upsert
    """

# dataset_id: a unique id for the dataset
    dataset_id: str = Field(default="")
# nebula_id: a unique id for the nebula
    nebula_id: str = Field(default="")
# nebula: the details of the nebula
    nebula: Nebula = Field(default_factory=Nebula)

class InsertDatasetFileRequest(BaseModel):
    """
     InsertDatasetFileRequest contains the dataset id to insert into and the
 dataset file details
    """

# dataset_id: the ID of the dataset to attach the file to
    dataset_id: str = Field(default="")
# files: the dataset files to insert
    files: typing.List[DatasetFile] = Field(default_factory=list)

class GetDatasetRequest(BaseModel):
    """
     GetDatasetRequest is the request message for getting the status of a dataset
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")

class GetDatasetResponse(BaseModel):
    """
     GetDatasetResponse is the response message for getting the status of a
 dataset
    """

# dataset: the dataset that is being built
    dataset: Dataset = Field(default_factory=Dataset)

class CancelGravityTaskRequest(BaseModel):
    """
     CancelGravityTaskRequest is the request message for cancelling a gravity task
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")

class CancelGravityTaskResponse(BaseModel):
    """
     CancelGravityTaskResponse is the response message for cancelling a gravity
 task
    """

# message: the message of the cancellation of the gravity task (currently
# hardcoded to "success")
    message: str = Field(default="")

class CancelDatasetRequest(BaseModel):
    """
     CancelDatasetRequest is the request message for cancelling a dataset build
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")

class CancelDatasetResponse(BaseModel):
    """
     CancelDatasetResponse is the response message for cancelling a dataset build
    """

# message: the message of the cancellation of the dataset build (currently
# hardcoded to "success")
    message: str = Field(default="")

class DatasetBillingCorrectionRequest(BaseModel):
    """
     DatasetBillingCorrectionRequest is the request message for refunding a user
    """

# requested_row_count: number of rows expected by the user
    requested_row_count: int = Field(default=0)
# actual_row_count: number of rows returned by gravity
    actual_row_count: int = Field(default=0)

class DatasetBillingCorrectionResponse(BaseModel):
    """
     DatasetBillingCorrectionResponse is the response message for refunding a user
    """

# refund_amount
    refund_amount: float = Field(default=0.0)

class GetMarketplaceDatasetsResponse(BaseModel):
    """
     GetMarketplaceDatasetsResponse returns the dataset metadata to be used in
 Marketplace
    """

# datasets: list of marketplace datasets
    datasets: typing.List[GravityMarketplaceTaskState] = Field(default_factory=list)

class GetGravityTaskDatasetFilesRequest(BaseModel):
    """
     GetGravityTaskDatasetFilesRequest is the request message for getting dataset
 files for a gravity task
    """

# gravity_task_id: the ID of the gravity task (required)
    gravity_task_id: str = Field(default="")

class DatasetFileWithId(BaseModel):
    """
     DatasetFileWithId extends DatasetFile to include the dataset ID
    """

# dataset_id: the ID of the dataset this file belongs to
    dataset_id: str = Field(default="")
# file_name: the name of the file
    file_name: str = Field(default="")
# file_size_bytes: the size of the file in bytes
    file_size_bytes: int = Field(default=0)
# last_modified: the date the file was last modified
    last_modified: datetime = Field(default_factory=datetime.now)
# num_rows: the number of rows in the file
    num_rows: int = Field(default=0)
# s3_key: the key of the file in S3 (internal use only)
    s3_key: str = Field(default="")
# url: the URL of the file (public use)
    url: str = Field(default="")
# nebula_url: the url of a nebula
    nebula_url: str = Field(default="")

class CrawlerDatasetFiles(BaseModel):
    """
     CrawlerDatasetFiles contains dataset files for a specific crawler
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")
# dataset_files: the dataset files associated with this crawler
    dataset_files: typing.List[DatasetFileWithId] = Field(default_factory=list)

class CrawlerRawMinerFilesResponse(BaseModel):
    """
     CrawlerRawMinerFiles contains raw miner files for a specific crawler
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")
# s3_paths: the S3 paths associated with this crawler
    s3_paths: typing.List[str] = Field(default_factory=list)

class GetGravityTaskDatasetFilesResponse(BaseModel):
    """
     GetGravityTaskDatasetFilesResponse is the response message for getting
 dataset files for a gravity task
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")
# crawler_dataset_files: dataset files grouped by crawler
    crawler_dataset_files: typing.List[CrawlerDatasetFiles] = Field(default_factory=list)

class GetCrawlerHistoryRequest(BaseModel):
    """
     GetCrawlerHistoryRequest is the request message for getting crawler history
 associated to the provided gravity_task_id
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")

class CrawlerHistoryEntry(BaseModel):
    """
     CrawlerHistoryEntry represents a single history entry for a crawler
    """

# ingest_dt: the timestamp when this entry was ingested
    ingest_dt: datetime = Field(default_factory=datetime.now)
# records_collected: the number of records collected
    records_collected: int = Field(default=0)
# bytes_collected: the number of bytes collected
    bytes_collected: int = Field(default=0)

class CrawlerCriteriaAndHistory(BaseModel):
    """
     CrawlerCriteriaAndHistory represents crawler information with criteria and
 history
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")
# platform: the platform from gravity_crawler_criteria
    platform: str = Field(default="")
# topic: the topic from gravity_crawler_criteria
    topic: typing.Optional[str] = Field(default="")
# keyword: the keyword from gravity_crawler_criteria
    keyword: typing.Optional[str] = Field(default="")
# post_start_date: the start date for posts from gravity_crawler_criteria
    post_start_date: typing.Optional[datetime] = Field(default_factory=datetime.now)
# post_end_date: the end date for posts from gravity_crawler_criteria
    post_end_date: typing.Optional[datetime] = Field(default_factory=datetime.now)
# crawler_history: the history entries for this crawler
    crawler_history: CrawlerHistoryEntry = Field(default_factory=CrawlerHistoryEntry)

class GetCrawlerHistoryResponse(BaseModel):
    """
     GetCrawlerHistoryResponse is the response message for getting crawler history
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")
# crawlers: the crawlers with their criteria and history
    crawlers: typing.List[CrawlerCriteriaAndHistory] = Field(default_factory=list)

class GetCrawlerDataForDDSubmissionRequest(BaseModel):
    """
     GetCrawlerDataForDDSubmissionRequest is the request message for getting crawler data
    """

# dsns: list of database connection strings to query
    dsns: typing.List[str] = Field(default_factory=list)

class CrawlerDataForDD(BaseModel):
    """
     CrawlerDataForDD contains crawler information for DD submission
    """

    crawler_id: str = Field(default="")
    platform: str = Field(default="")
    topic: typing.Optional[str] = Field(default="")
    keyword: typing.Optional[str] = Field(default="")
    post_start_datetime: typing.Optional[str] = Field(default="")
    post_end_datetime: typing.Optional[str] = Field(default="")

class GetCrawlerDataForDDSubmissionResponse(BaseModel):
    """
     GetCrawlerDataForDDSubmissionResponse is the response message for crawler data
    """

# crawlers: list of crawler data for DD submission
    crawlers: typing.List[CrawlerDataForDD] = Field(default_factory=list)
