from typing import Dict, List, Union

import grpc

from macrocosmos import __package_name__, __version__
from macrocosmos.generated.gravity.v1 import gravity_p2p, gravity_pb2, gravity_pb2_grpc
from macrocosmos.types import MacrocosmosError
from macrocosmos.resources._client import BaseClient
from macrocosmos.resources._utils import run_sync_threadsafe


class AsyncGravity:
    """Asynchronous Gravity resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client: BaseClient):
        """
        Initialize the asynchronous Gravity resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client

    async def GetGravityTasks(
        self,
        gravity_task_id: str = "",
        include_crawlers: bool = False,
    ) -> gravity_pb2.GetGravityTasksResponse:
        """
        List all gravity tasks for a user.

        Args:
            gravity_task_id: The ID of the gravity task (optional, if not provided, all gravity tasks for the user will be returned).
            include_crawlers: Whether to include the crawler states in the response. (default: False)

        Returns:
            A response containing the gravity tasks.
        """
        request = gravity_pb2.GetGravityTasksRequest(
            gravity_task_id=gravity_task_id,
            include_crawlers=include_crawlers,
        )

        return await self._make_request("GetGravityTasks", request)

    async def GetCrawler(
        self,
        crawler_id: str,
    ) -> gravity_pb2.GetCrawlerResponse:
        """
        Get a single crawler by its ID.

        Args:
            crawler_id: The ID of the crawler to get.

        Returns:
            A response containing the crawler details.
        """
        if not crawler_id:
            raise AttributeError("crawler_id is a required parameter")

        request = gravity_pb2.GetCrawlerRequest(crawler_id=crawler_id)

        return await self._make_request("GetCrawler", request)

    async def CreateGravityTask(
        self,
        gravity_tasks: List[Union[gravity_p2p.GravityTask, Dict]] = None,
        name: str = "",
        notification_requests: List[
            Union[gravity_p2p.NotificationRequest, Dict]
        ] = None,
        gravity_task_id: str = "",
    ) -> gravity_pb2.CreateGravityTaskResponse:
        """
        Create a new gravity task.

        Args:
            gravity_tasks: The list of gravity task criteria for the crawlers.
            name: The name of the gravity task (optional).
            notification_requests: The details of the notifications to be sent (optional).
            gravity_task_id: The ID of the gravity task (optional).

        Returns:
            A response containing the ID of the created gravity task.
        """
        proto_gravity_tasks = []
        if gravity_tasks:
            for task in gravity_tasks:
                if isinstance(task, gravity_p2p.GravityTask):
                    proto_gravity_tasks.append(
                        gravity_pb2.GravityTask(**task.model_dump())
                    )
                elif isinstance(task, dict):
                    proto_gravity_tasks.append(gravity_pb2.GravityTask(**task))
                else:
                    raise TypeError(f"Invalid type for gravity task: {type(task)}")
        else:
            raise AttributeError("gravity_tasks is a required parameter")

        proto_notification_requests = []
        if notification_requests:
            for notification in notification_requests:
                if isinstance(notification, gravity_p2p.NotificationRequest):
                    proto_notification_requests.append(
                        gravity_pb2.NotificationRequest(**notification.model_dump())
                    )
                elif isinstance(notification, dict):
                    proto_notification_requests.append(
                        gravity_pb2.NotificationRequest(**notification)
                    )
                else:
                    raise TypeError(
                        f"Invalid type for notification request: {type(notification)}"
                    )

        request = gravity_pb2.CreateGravityTaskRequest(
            gravity_tasks=proto_gravity_tasks,
            name=name,
            notification_requests=proto_notification_requests,
            gravity_task_id=gravity_task_id,
        )

        return await self._make_request("CreateGravityTask", request)

    async def BuildDataset(
        self,
        crawler_id: str,
        max_rows: int,
        notification_requests: List[
            Union[gravity_p2p.NotificationRequest, Dict]
        ] = None,
    ) -> gravity_pb2.BuildDatasetResponse:
        """
        Build a dataset for a single crawler.

        Args:
            crawler_id: The ID of the crawler to build a dataset for.
            max_rows: The maximum number of rows to include in the dataset.
            notification_requests: The details of the notifications to be sent (optional).
        Returns:
            A response containing the dataset that was built.
        """
        if not crawler_id:
            raise AttributeError("crawler_id is a required parameter")

        proto_notification_requests = []
        if notification_requests:
            for notification in notification_requests:
                if isinstance(notification, gravity_p2p.NotificationRequest):
                    proto_notification_requests.append(
                        gravity_pb2.NotificationRequest(**notification.model_dump())
                    )
                elif isinstance(notification, dict):
                    proto_notification_requests.append(
                        gravity_pb2.NotificationRequest(**notification)
                    )
                else:
                    raise TypeError(
                        f"Invalid type for notification request: {type(notification)}"
                    )

        request = gravity_pb2.BuildDatasetRequest(
            crawler_id=crawler_id,
            max_rows=max_rows,
            notification_requests=proto_notification_requests,
        )

        return await self._make_request("BuildDataset", request)

    async def GetDataset(
        self,
        dataset_id: str,
    ) -> gravity_pb2.GetDatasetResponse:
        """
        Get the status of a dataset.

        Args:
            dataset_id: The ID of the dataset to get the status for.

        Returns:
            A response containing the dataset status.
        """
        if not dataset_id:
            raise AttributeError("dataset_id is a required parameter")

        request = gravity_pb2.GetDatasetRequest(
            dataset_id=dataset_id,
        )

        return await self._make_request("GetDataset", request)

    async def CancelGravityTask(
        self,
        gravity_task_id: str,
    ) -> gravity_pb2.CancelGravityTaskResponse:
        """
        Cancel a gravity task.

        Args:
            gravity_task_id: The ID of the gravity task to cancel.

        Returns:
            A response containing the cancellation status.
        """
        if not gravity_task_id:
            raise AttributeError("gravity_task_id is a required parameter")

        request = gravity_pb2.CancelGravityTaskRequest(
            gravity_task_id=gravity_task_id,
        )

        return await self._make_request("CancelGravityTask", request)

    async def CancelDataset(
        self,
        dataset_id: str,
    ) -> gravity_pb2.CancelDatasetResponse:
        """
        Cancel a dataset.

        Args:
            dataset_id: The ID of the dataset to cancel.

        Returns:
            A response containing the cancellation status.
        """
        if not dataset_id:
            raise AttributeError("dataset_id is a required parameter")

        request = gravity_pb2.CancelDatasetRequest(
            dataset_id=dataset_id,
        )

        return await self._make_request("CancelDataset", request)

    async def _make_request(self, method_name, request):
        """
        Make a request to the Gravity service.

        Args:
            method_name: The name of the method to call.
            request: The request message.

        Returns:
            The response from the service.
        """
        metadata = [
            ("x-source", self._client.app_name),
            ("x-client-id", __package_name__),
            ("x-client-version", __version__),
            ("authorization", f"Bearer {self._client.api_key}"),
        ]

        compression = grpc.Compression.Gzip if self._client.compress else None

        retries = 0
        last_error = None
        while retries <= self._client.max_retries:
            channel = None
            try:
                channel = self._client.get_async_channel()
                stub = gravity_pb2_grpc.GravityServiceStub(channel)
                method = getattr(stub, method_name)
                response = await method(
                    request,
                    metadata=metadata,
                    timeout=self._client.timeout,
                    compression=compression,
                )
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
            except Exception as e:
                raise MacrocosmosError(f"Error calling {method_name}: {e}")
            finally:
                if channel:
                    await channel.close()

        raise last_error


class SyncGravity:
    """Synchronous Gravity resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client: BaseClient):
        """
        Initialize the synchronous Gravity resource.

        Args:
            client: The client to use for the resource.
        """
        self._client = client
        self._async_gravity = AsyncGravity(client)

    def GetGravityTasks(
        self,
        gravity_task_id: str = "",
        include_crawlers: bool = False,
    ) -> gravity_pb2.GetGravityTasksResponse:
        """
        List all gravity tasks for a user synchronously.

        Args:
            gravity_task_id: The ID of the gravity task (optional, if not provided, all gravity tasks for the user will be returned).
            include_crawlers: Whether to include the crawler states in the response.

        Returns:
            A response containing the gravity tasks.
        """
        return run_sync_threadsafe(
            self._async_gravity.GetGravityTasks(
                gravity_task_id=gravity_task_id,
                include_crawlers=include_crawlers,
            )
        )

    def CreateGravityTask(
        self,
        gravity_tasks: List[Union[gravity_p2p.GravityTask, Dict]] = None,
        name: str = "",
        notification_requests: List[
            Union[gravity_p2p.NotificationRequest, Dict]
        ] = None,
        gravity_task_id: str = "",
    ) -> gravity_pb2.CreateGravityTaskResponse:
        """
        Create a new gravity task synchronously.

        Args:
            gravity_tasks: The list of gravity task criteria for the crawlers.
            name: The name of the gravity task (optional).
            notification_requests: The details of the notifications to be sent (optional).
            gravity_task_id: The ID of the gravity task (optional).

        Returns:
            A response containing the ID of the created gravity task.
        """
        return run_sync_threadsafe(
            self._async_gravity.CreateGravityTask(
                gravity_tasks=gravity_tasks,
                name=name,
                notification_requests=notification_requests,
                gravity_task_id=gravity_task_id,
            )
        )

    def BuildDataset(
        self,
        crawler_id: str,
        max_rows: int,
        notification_requests: List[
            Union[gravity_p2p.NotificationRequest, Dict]
        ] = None,
    ) -> gravity_pb2.BuildDatasetResponse:
        """
        Build a dataset for a single crawler synchronously.

        Args:
            crawler_id: The ID of the crawler to build a dataset for.
            max_rows: The maximum number of rows to include in the dataset.
            notification_requests: The details of the notifications to be sent (optional).

        Returns:
            A response containing the dataset that was built.
        """
        return run_sync_threadsafe(
            self._async_gravity.BuildDataset(
                crawler_id=crawler_id,
                max_rows=max_rows,
                notification_requests=notification_requests,
            )
        )

    def GetDataset(
        self,
        dataset_id: str,
    ) -> gravity_pb2.GetDatasetResponse:
        """
        Get the status of a dataset build synchronously.

        Args:
            dataset_id: The ID of the dataset to get the status for.

        Returns:
            A response containing the dataset status.
        """
        return run_sync_threadsafe(
            self._async_gravity.GetDataset(
                dataset_id=dataset_id,
            )
        )

    def CancelGravityTask(
        self,
        gravity_task_id: str,
    ) -> gravity_pb2.CancelGravityTaskResponse:
        """
        Cancel a gravity task synchronously.

        Args:
            gravity_task_id: The ID of the gravity task to cancel.

        Returns:
            A response containing the cancellation status.
        """
        return run_sync_threadsafe(
            self._async_gravity.CancelGravityTask(
                gravity_task_id=gravity_task_id,
            )
        )

    def CancelDataset(
        self,
        dataset_id: str,
    ) -> gravity_pb2.CancelDatasetResponse:
        """
        Cancel a dataset build synchronously.
        """
        return run_sync_threadsafe(
            self._async_gravity.CancelDataset(
                dataset_id=dataset_id,
            )
        )
