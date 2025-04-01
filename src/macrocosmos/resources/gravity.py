import asyncio
import grpc
import random
from typing import Dict, List, Optional, Union

from macrocosmos import __version__, __package_name__
from macrocosmos.types import MacrocosmosError
from macrocosmos.generated.gravity.v1 import gravity_pb2, gravity_p2p, gravity_pb2_grpc


class AsyncGravity:
    """Asynchronous Gravity resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client):
        self._client = client

    async def GetGravityTasks(
        self,
        gravity_task_id: str = "",
        include_crawlers: bool = False,
        **kwargs,
    ) -> gravity_pb2.GetGravityTasksResponse:
        """
        List all gravity tasks for a user.

        Args:
            gravity_task_id: The ID of the gravity task (optional, if not provided, all gravity tasks for the user will be returned).
            include_crawlers: Whether to include the crawler states in the response.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the gravity tasks.
        """
        request = gravity_pb2.GetGravityTasksRequest(
            gravity_task_id=gravity_task_id,
            include_crawlers=include_crawlers,
            **kwargs,
        )

        return await self._make_request("GetGravityTasks", request)

    async def CreateGravityTask(
        self,
        gravity_tasks: List[Union[gravity_p2p.GravityTask, Dict]] = None,
        name: str = "",
        user: Union[gravity_p2p.User, Dict] = None,
        notification_requests: List[Union[gravity_p2p.NotificationRequest, Dict]] = None,
        gravity_task_id: str = "",
        **kwargs,
    ) -> gravity_pb2.CreateGravityTaskResponse:
        """
        Create a new gravity task.

        Args:
            gravity_tasks: The list of gravity task criteria for the crawlers.
            name: The name of the gravity task (optional).
            user: The user who is creating the gravity task (optional).
            notification_requests: The details of the notifications to be sent (optional).
            gravity_task_id: The ID of the gravity task (optional).
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the ID of the created gravity task.
        """
        proto_gravity_tasks = []
        if gravity_tasks:
            for task in gravity_tasks:
                if isinstance(task, gravity_p2p.GravityTask):
                    proto_gravity_tasks.append(gravity_pb2.GravityTask(**task.model_dump()))
                elif isinstance(task, dict):
                    proto_gravity_tasks.append(gravity_pb2.GravityTask(**task))
                else:
                    raise TypeError(f"Invalid type for gravity task: {type(task)}")
        else:
            raise AttributeError("gravity_tasks is a required parameter")

        proto_user = None
        if user:
            if isinstance(user, gravity_p2p.User):
                proto_user = gravity_pb2.User(**user.model_dump())
            elif isinstance(user, dict):
                proto_user = gravity_pb2.User(**user)
            else:
                raise TypeError(f"Invalid type for user: {type(user)}")
        else:
            proto_user = gravity_pb2.User()

        proto_notification_requests = []
        if notification_requests:
            for notification in notification_requests:
                if isinstance(notification, gravity_p2p.NotificationRequest):
                    proto_notification_requests.append(gravity_pb2.NotificationRequest(**notification.model_dump()))
                elif isinstance(notification, dict):
                    proto_notification_requests.append(gravity_pb2.NotificationRequest(**notification))
                else:
                    raise TypeError(f"Invalid type for notification request: {type(notification)}")

        request = gravity_pb2.CreateGravityTaskRequest(
            gravity_tasks=proto_gravity_tasks,
            name=name,
            user=proto_user,
            notification_requests=proto_notification_requests,
            gravity_task_id=gravity_task_id,
            **kwargs,
        )

        return await self._make_request("CreateGravityTask", request)

    async def BuildDataset(
        self,
        crawler_id: str,
        notification_requests: List[Union[gravity_p2p.NotificationRequest, Dict]] = None,
        **kwargs,
    ) -> gravity_pb2.BuildDatasetResponse:
        """
        Build a dataset for a single crawler.

        Args:
            crawler_id: The ID of the crawler to build a dataset for.
            notification_requests: The details of the notifications to be sent (optional).
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the dataset that was built.
        """
        if not crawler_id:
            raise AttributeError("crawler_id is a required parameter")

        proto_notification_requests = []
        if notification_requests:
            for notification in notification_requests:
                if isinstance(notification, gravity_p2p.NotificationRequest):
                    proto_notification_requests.append(gravity_pb2.NotificationRequest(**notification.model_dump()))
                elif isinstance(notification, dict):
                    proto_notification_requests.append(gravity_pb2.NotificationRequest(**notification))
                else:
                    raise TypeError(f"Invalid type for notification request: {type(notification)}")

        request = gravity_pb2.BuildDatasetRequest(
            crawler_id=crawler_id,
            notification_requests=proto_notification_requests,
            **kwargs,
        )

        return await self._make_request("BuildDataset", request)

    async def GetDatasetStatus(
        self,
        dataset_id: str,
        **kwargs,
    ) -> gravity_pb2.GetDatasetStatusResponse:
        """
        Get the status of a dataset build.

        Args:
            dataset_id: The ID of the dataset to get the status for.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the dataset status.
        """
        if not dataset_id:
            raise AttributeError("dataset_id is a required parameter")

        request = gravity_pb2.GetDatasetStatusRequest(
            dataset_id=dataset_id,
            **kwargs,
        )

        return await self._make_request("GetDatasetStatus", request)

    async def CancelGravityTask(
        self,
        gravity_task_id: str,
        **kwargs,
    ) -> gravity_pb2.CancelGravityTaskResponse:
        """
        Cancel a gravity task.

        Args:
            gravity_task_id: The ID of the gravity task to cancel.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the cancellation status.
        """
        if not gravity_task_id:
            raise AttributeError("gravity_task_id is a required parameter")

        request = gravity_pb2.CancelGravityTaskRequest(
            gravity_task_id=gravity_task_id,
            **kwargs,
        )

        return await self._make_request("CancelGravityTask", request)

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
            ("x-client-id", __package_name__),
            ("x-client-version", __version__),
            ("authorization", f"Bearer {self._client.api_key}"),
        ]

        compression = grpc.Compression.Gzip if self._client.compress else None

        retries = 0
        last_error = None
        while retries <= self._client.max_retries:
            try:
                channel = grpc.aio.secure_channel(self._client.base_url, grpc.ssl_channel_credentials())
                stub = gravity_pb2_grpc.GravityServiceStub(channel)
                method = getattr(stub, method_name)
                response = await method(
                    request,
                    metadata=metadata,
                    timeout=self._client.timeout,
                    compression=compression,
                )
                await channel.close()
                return response
            except grpc.RpcError as e:
                last_error = MacrocosmosError(f"RPC error: {e.code()}: {e.details()}")
                retries += 1
                await channel.close()
            except Exception as e:
                await channel.close()
                raise MacrocosmosError(f"Error calling {method_name}: {e}")

        raise last_error


class SyncGravity:
    """Synchronous Gravity resource for the Data Universe (subnet 13) API on Bittensor."""

    def __init__(self, client):
        self._client = client
        self._async_gravity = AsyncGravity(client)

    def GetGravityTasks(
        self,
        gravity_task_id: str = "",
        include_crawlers: bool = False,
        **kwargs,
    ) -> gravity_pb2.GetGravityTasksResponse:
        """
        List all gravity tasks for a user synchronously.

        Args:
            gravity_task_id: The ID of the gravity task (optional, if not provided, all gravity tasks for the user will be returned).
            include_crawlers: Whether to include the crawler states in the response.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the gravity tasks.
        """
        return asyncio.run(
            self._async_gravity.GetGravityTasks(
                gravity_task_id=gravity_task_id,
                include_crawlers=include_crawlers,
                **kwargs,
            )
        )

    def CreateGravityTask(
        self,
        gravity_tasks: List[Union[gravity_p2p.GravityTask, Dict]] = None,
        name: str = "",
        user: Union[gravity_p2p.User, Dict] = None,
        notification_requests: List[Union[gravity_p2p.NotificationRequest, Dict]] = None,
        gravity_task_id: str = "",
        **kwargs,
    ) -> gravity_pb2.CreateGravityTaskResponse:
        """
        Create a new gravity task synchronously.

        Args:
            gravity_tasks: The list of gravity task criteria for the crawlers.
            name: The name of the gravity task (optional).
            user: The user who is creating the gravity task (optional).
            notification_requests: The details of the notifications to be sent (optional).
            gravity_task_id: The ID of the gravity task (optional).
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the ID of the created gravity task.
        """
        return asyncio.run(
            self._async_gravity.CreateGravityTask(
                gravity_tasks=gravity_tasks,
                name=name,
                user=user,
                notification_requests=notification_requests,
                gravity_task_id=gravity_task_id,
                **kwargs,
            )
        )

    def BuildDataset(
        self,
        crawler_id: str,
        notification_requests: List[Union[gravity_p2p.NotificationRequest, Dict]] = None,
        **kwargs,
    ) -> gravity_pb2.BuildDatasetResponse:
        """
        Build a dataset for a single crawler synchronously.

        Args:
            crawler_id: The ID of the crawler to build a dataset for.
            notification_requests: The details of the notifications to be sent (optional).
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the dataset that was built.
        """
        return asyncio.run(
            self._async_gravity.BuildDataset(
                crawler_id=crawler_id,
                notification_requests=notification_requests,
                **kwargs,
            )
        )

    def GetDatasetStatus(
        self,
        dataset_id: str,
        **kwargs,
    ) -> gravity_pb2.GetDatasetStatusResponse:
        """
        Get the status of a dataset build synchronously.

        Args:
            dataset_id: The ID of the dataset to get the status for.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the dataset status.
        """
        return asyncio.run(
            self._async_gravity.GetDatasetStatus(
                dataset_id=dataset_id,
                **kwargs,
            )
        )

    def CancelGravityTask(
        self,
        gravity_task_id: str,
        **kwargs,
    ) -> gravity_pb2.CancelGravityTaskResponse:
        """
        Cancel a gravity task synchronously.

        Args:
            gravity_task_id: The ID of the gravity task to cancel.
            **kwargs: Additional parameters to include in the request.

        Returns:
            A response containing the cancellation status.
        """
        return asyncio.run(
            self._async_gravity.CancelGravityTask(
                gravity_task_id=gravity_task_id,
                **kwargs,
            )
        )
