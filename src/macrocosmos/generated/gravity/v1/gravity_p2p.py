# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


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
     Crawler is a single crawler workflow that registers a single job (platform/topic) on SN13's dynamic desirability engine
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
# dataset_workflows: the IDs of the dataset workflows that are associated with the crawler
    dataset_workflows: typing.List[str] = Field(default_factory=list)

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
# crawler_ids: the IDs of the crawler workflows that are associated with the gravity task
    crawler_ids: typing.List[str] = Field(default_factory=list)
# crawler_workflows: the crawler workflows that are associated with the gravity task
    crawler_workflows: typing.List[Crawler] = Field(default_factory=list)

class GetGravityTasksRequest(BaseModel):
    """
     GetGravityTasksRequest is the request message for listing gravity tasks for a user
    """

# gravity_task_id: the ID of the gravity task (optional, if not provided, all gravity tasks for the user will be returned)
    gravity_task_id: typing.Optional[str] = Field(default="")
# include_crawlers: whether to include the crawler states in the response
    include_crawlers: typing.Optional[bool] = Field(default=False)

class GetGravityTasksResponse(BaseModel):
    """
     GetGravityTasksResponse is the response message for listing gravity tasks for a user
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
     NotificationRequest is the request message for sending a notification to a user when a dataset is ready to download
    """

# type: the type of notification to send ('email' is only supported currently)
    type: str = Field(default="")
# address: the address to send the notification to (only email addresses are supported currently)
    address: str = Field(default="")
# redirect_url: the URL to include in the notication message that redirects the user to any built datasets
    redirect_url: typing.Optional[str] = Field(default="")

class GetCrawlerRequest(BaseModel):
    """
     GetCrawlerRequest is the request message for getting a crawler
    """

# crawler_id: the ID of the crawler
    crawler_id: str = Field(default="")

class GetCrawlerResponse(BaseModel):
    """
     GetCrawlerResponse is the response message for getting a crawler
    """

# crawler: the crawler
    crawler: Crawler = Field(default_factory=Crawler)

class CreateGravityTaskRequest(BaseModel):
    """
     CreateGravityTaskRequest is the request message for creating a new gravity task
    """

# gravity_tasks: the criteria for the crawlers that will be created
    gravity_tasks: typing.List[GravityTask] = Field(default_factory=list)
# name: the name of the gravity task (optional, default will generate a random name)
    name: str = Field(default="")
# notification_requests: the details of the notification to be sent to the user when a dataset
#   that is automatically generated upon completion of the crawler is ready to download (optional)
    notification_requests: typing.List[NotificationRequest] = Field(default_factory=list)
# gravity_task_id: the ID of the gravity task (optional, default will generate a random ID)
    gravity_task_id: typing.Optional[str] = Field(default="")

class CreateGravityTaskResponse(BaseModel):
    """
     CreateGravityTaskResponse is the response message for creating a new gravity task
    """

# gravity_task_id: the ID of the gravity task
    gravity_task_id: str = Field(default="")

class BuildDatasetRequest(BaseModel):
    """
     BuildDatasetRequest is the request message for manually requesting the building of a dataset for a single crawler
    """

# crawler_id: the ID of the crawler that will be used to build the dataset
    crawler_id: str = Field(default="")
# notification_requests: the details of the notification to be sent to the user when the dataset is ready to download (optional)
    notification_requests: typing.List[NotificationRequest] = Field(default_factory=list)
# max_rows: the maximum number of rows to include in the dataset (optional, defaults to 500)
    max_rows: int = Field(default=0)

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
     BuildDatasetResponse is the response message for manually requesting the building of a dataset for a single crawler
 - dataset: the dataset that was built
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")
# dataset: the dataset that was built
    dataset: Dataset = Field(default_factory=Dataset)

class GetDatasetRequest(BaseModel):
    """
     GetDatasetRequest is the request message for getting the status of a dataset
    """

# dataset_id: the ID of the dataset
    dataset_id: str = Field(default="")

class GetDatasetResponse(BaseModel):
    """
     GetDatasetResponse is the response message for getting the status of a dataset
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
     CancelGravityTaskResponse is the response message for cancelling a gravity task
    """

# message: the message of the cancellation of the gravity task (currently hardcoded to "success")
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

# message: the message of the cancellation of the dataset build (currently hardcoded to "success")
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
