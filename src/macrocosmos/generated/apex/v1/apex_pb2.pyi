from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ChatCompletionRequest(_message.Message):
    __slots__ = ("uids", "messages", "seed", "task", "model", "test_time_inference", "mixture", "sampling_parameters", "inference_mode", "json_format", "stream", "timeout")
    UIDS_FIELD_NUMBER: _ClassVar[int]
    MESSAGES_FIELD_NUMBER: _ClassVar[int]
    SEED_FIELD_NUMBER: _ClassVar[int]
    TASK_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    TEST_TIME_INFERENCE_FIELD_NUMBER: _ClassVar[int]
    MIXTURE_FIELD_NUMBER: _ClassVar[int]
    SAMPLING_PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    INFERENCE_MODE_FIELD_NUMBER: _ClassVar[int]
    JSON_FORMAT_FIELD_NUMBER: _ClassVar[int]
    STREAM_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    uids: _containers.RepeatedScalarFieldContainer[int]
    messages: _containers.RepeatedCompositeFieldContainer[ChatMessage]
    seed: int
    task: str
    model: str
    test_time_inference: bool
    mixture: bool
    sampling_parameters: SamplingParameters
    inference_mode: str
    json_format: bool
    stream: bool
    timeout: int
    def __init__(self, uids: _Optional[_Iterable[int]] = ..., messages: _Optional[_Iterable[_Union[ChatMessage, _Mapping]]] = ..., seed: _Optional[int] = ..., task: _Optional[str] = ..., model: _Optional[str] = ..., test_time_inference: bool = ..., mixture: bool = ..., sampling_parameters: _Optional[_Union[SamplingParameters, _Mapping]] = ..., inference_mode: _Optional[str] = ..., json_format: bool = ..., stream: bool = ..., timeout: _Optional[int] = ...) -> None: ...

class SamplingParameters(_message.Message):
    __slots__ = ("temperature", "top_p", "top_k", "max_new_tokens", "do_sample")
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    TOP_P_FIELD_NUMBER: _ClassVar[int]
    TOP_K_FIELD_NUMBER: _ClassVar[int]
    MAX_NEW_TOKENS_FIELD_NUMBER: _ClassVar[int]
    DO_SAMPLE_FIELD_NUMBER: _ClassVar[int]
    temperature: float
    top_p: float
    top_k: float
    max_new_tokens: int
    do_sample: bool
    def __init__(self, temperature: _Optional[float] = ..., top_p: _Optional[float] = ..., top_k: _Optional[float] = ..., max_new_tokens: _Optional[int] = ..., do_sample: bool = ...) -> None: ...

class ChatCompletionResponse(_message.Message):
    __slots__ = ("id", "choices", "created", "model", "object", "service_tier", "system_fingerprint", "usage")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TIER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    choices: _containers.RepeatedCompositeFieldContainer[Choice]
    created: int
    model: str
    object: str
    service_tier: str
    system_fingerprint: str
    usage: CompletionUsage
    def __init__(self, id: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[Choice, _Mapping]]] = ..., created: _Optional[int] = ..., model: _Optional[str] = ..., object: _Optional[str] = ..., service_tier: _Optional[str] = ..., system_fingerprint: _Optional[str] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ...) -> None: ...

class Choice(_message.Message):
    __slots__ = ("finish_reason", "index", "logprobs", "message")
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    finish_reason: str
    index: int
    logprobs: ChoiceLogprobs
    message: ChatCompletionMessage
    def __init__(self, finish_reason: _Optional[str] = ..., index: _Optional[int] = ..., logprobs: _Optional[_Union[ChoiceLogprobs, _Mapping]] = ..., message: _Optional[_Union[ChatCompletionMessage, _Mapping]] = ...) -> None: ...

class ChatCompletionMessage(_message.Message):
    __slots__ = ("content", "refusal", "role", "annotations", "audio", "function_call", "tool_calls")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    REFUSAL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    ANNOTATIONS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    content: str
    refusal: str
    role: str
    annotations: _containers.RepeatedCompositeFieldContainer[Annotation]
    audio: ChatCompletionAudio
    function_call: FunctionCall
    tool_calls: _containers.RepeatedCompositeFieldContainer[ChatCompletionMessageToolCall]
    def __init__(self, content: _Optional[str] = ..., refusal: _Optional[str] = ..., role: _Optional[str] = ..., annotations: _Optional[_Iterable[_Union[Annotation, _Mapping]]] = ..., audio: _Optional[_Union[ChatCompletionAudio, _Mapping]] = ..., function_call: _Optional[_Union[FunctionCall, _Mapping]] = ..., tool_calls: _Optional[_Iterable[_Union[ChatCompletionMessageToolCall, _Mapping]]] = ...) -> None: ...

class Annotation(_message.Message):
    __slots__ = ("content", "role")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    content: str
    role: str
    def __init__(self, content: _Optional[str] = ..., role: _Optional[str] = ...) -> None: ...

class ChatCompletionAudio(_message.Message):
    __slots__ = ("id", "data", "expires_at", "transcript")
    ID_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_AT_FIELD_NUMBER: _ClassVar[int]
    TRANSCRIPT_FIELD_NUMBER: _ClassVar[int]
    id: str
    data: str
    expires_at: int
    transcript: str
    def __init__(self, id: _Optional[str] = ..., data: _Optional[str] = ..., expires_at: _Optional[int] = ..., transcript: _Optional[str] = ...) -> None: ...

class FunctionCall(_message.Message):
    __slots__ = ("arguments", "name")
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, arguments: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ...) -> None: ...

class ChatCompletionMessageToolCall(_message.Message):
    __slots__ = ("id", "function", "type")
    ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    function: Function
    type: str
    def __init__(self, id: _Optional[str] = ..., function: _Optional[_Union[Function, _Mapping]] = ..., type: _Optional[str] = ...) -> None: ...

class Function(_message.Message):
    __slots__ = ("arguments", "name")
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, arguments: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ...) -> None: ...

class ChatCompletionChunkResponse(_message.Message):
    __slots__ = ("id", "choices", "created", "model", "object", "service_tier", "system_fingerprint", "usage")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHOICES_FIELD_NUMBER: _ClassVar[int]
    CREATED_FIELD_NUMBER: _ClassVar[int]
    MODEL_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TIER_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    USAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    choices: _containers.RepeatedCompositeFieldContainer[ChunkChoice]
    created: int
    model: str
    object: str
    service_tier: str
    system_fingerprint: str
    usage: CompletionUsage
    def __init__(self, id: _Optional[str] = ..., choices: _Optional[_Iterable[_Union[ChunkChoice, _Mapping]]] = ..., created: _Optional[int] = ..., model: _Optional[str] = ..., object: _Optional[str] = ..., service_tier: _Optional[str] = ..., system_fingerprint: _Optional[str] = ..., usage: _Optional[_Union[CompletionUsage, _Mapping]] = ...) -> None: ...

class ChatMessage(_message.Message):
    __slots__ = ("role", "content")
    ROLE_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    role: str
    content: str
    def __init__(self, role: _Optional[str] = ..., content: _Optional[str] = ...) -> None: ...

class ChunkChoice(_message.Message):
    __slots__ = ("delta", "finish_reason", "index", "logprobs")
    DELTA_FIELD_NUMBER: _ClassVar[int]
    FINISH_REASON_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    delta: ChoiceDelta
    finish_reason: str
    index: int
    logprobs: ChoiceLogprobs
    def __init__(self, delta: _Optional[_Union[ChoiceDelta, _Mapping]] = ..., finish_reason: _Optional[str] = ..., index: _Optional[int] = ..., logprobs: _Optional[_Union[ChoiceLogprobs, _Mapping]] = ...) -> None: ...

class ChoiceLogprobs(_message.Message):
    __slots__ = ("content", "refusal")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    REFUSAL_FIELD_NUMBER: _ClassVar[int]
    content: _containers.RepeatedCompositeFieldContainer[ChatCompletionTokenLogprob]
    refusal: _containers.RepeatedCompositeFieldContainer[ChatCompletionTokenLogprob]
    def __init__(self, content: _Optional[_Iterable[_Union[ChatCompletionTokenLogprob, _Mapping]]] = ..., refusal: _Optional[_Iterable[_Union[ChatCompletionTokenLogprob, _Mapping]]] = ...) -> None: ...

class ChoiceDelta(_message.Message):
    __slots__ = ("content", "function_call", "refusal", "role", "tool_calls")
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_CALL_FIELD_NUMBER: _ClassVar[int]
    REFUSAL_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    TOOL_CALLS_FIELD_NUMBER: _ClassVar[int]
    content: str
    function_call: ChoiceDeltaFunctionCall
    refusal: str
    role: str
    tool_calls: _containers.RepeatedCompositeFieldContainer[ChoiceDeltaToolCall]
    def __init__(self, content: _Optional[str] = ..., function_call: _Optional[_Union[ChoiceDeltaFunctionCall, _Mapping]] = ..., refusal: _Optional[str] = ..., role: _Optional[str] = ..., tool_calls: _Optional[_Iterable[_Union[ChoiceDeltaToolCall, _Mapping]]] = ...) -> None: ...

class ChoiceDeltaFunctionCall(_message.Message):
    __slots__ = ("arguments", "name")
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, arguments: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ...) -> None: ...

class ChoiceDeltaToolCall(_message.Message):
    __slots__ = ("index", "id", "function", "type")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    index: int
    id: str
    function: ChoiceDeltaToolCallFunction
    type: str
    def __init__(self, index: _Optional[int] = ..., id: _Optional[str] = ..., function: _Optional[_Union[ChoiceDeltaToolCallFunction, _Mapping]] = ..., type: _Optional[str] = ...) -> None: ...

class ChoiceDeltaToolCallFunction(_message.Message):
    __slots__ = ("arguments", "name")
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    arguments: _containers.RepeatedScalarFieldContainer[str]
    name: str
    def __init__(self, arguments: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ...) -> None: ...

class ChatCompletionTokenLogprob(_message.Message):
    __slots__ = ("token", "bytes", "logprob", "top_logprobs")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    LOGPROB_FIELD_NUMBER: _ClassVar[int]
    TOP_LOGPROBS_FIELD_NUMBER: _ClassVar[int]
    token: str
    bytes: _containers.RepeatedScalarFieldContainer[int]
    logprob: float
    top_logprobs: _containers.RepeatedCompositeFieldContainer[TopLogprob]
    def __init__(self, token: _Optional[str] = ..., bytes: _Optional[_Iterable[int]] = ..., logprob: _Optional[float] = ..., top_logprobs: _Optional[_Iterable[_Union[TopLogprob, _Mapping]]] = ...) -> None: ...

class TopLogprob(_message.Message):
    __slots__ = ("token", "bytes", "logprob")
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    LOGPROB_FIELD_NUMBER: _ClassVar[int]
    token: str
    bytes: _containers.RepeatedScalarFieldContainer[int]
    logprob: float
    def __init__(self, token: _Optional[str] = ..., bytes: _Optional[_Iterable[int]] = ..., logprob: _Optional[float] = ...) -> None: ...

class CompletionUsage(_message.Message):
    __slots__ = ("completion_tokens", "prompt_tokens", "total_tokens", "completion_tokens_details", "prompt_tokens_details")
    COMPLETION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKENS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TOKENS_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TOKENS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    PROMPT_TOKENS_DETAILS_FIELD_NUMBER: _ClassVar[int]
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int
    completion_tokens_details: CompletionTokensDetails
    prompt_tokens_details: PromptTokensDetails
    def __init__(self, completion_tokens: _Optional[int] = ..., prompt_tokens: _Optional[int] = ..., total_tokens: _Optional[int] = ..., completion_tokens_details: _Optional[_Union[CompletionTokensDetails, _Mapping]] = ..., prompt_tokens_details: _Optional[_Union[PromptTokensDetails, _Mapping]] = ...) -> None: ...

class CompletionTokensDetails(_message.Message):
    __slots__ = ("accepted_prediction_tokens", "audio_tokens", "reasoning_tokens", "rejected_prediction_tokens")
    ACCEPTED_PREDICTION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    AUDIO_TOKENS_FIELD_NUMBER: _ClassVar[int]
    REASONING_TOKENS_FIELD_NUMBER: _ClassVar[int]
    REJECTED_PREDICTION_TOKENS_FIELD_NUMBER: _ClassVar[int]
    accepted_prediction_tokens: int
    audio_tokens: int
    reasoning_tokens: int
    rejected_prediction_tokens: int
    def __init__(self, accepted_prediction_tokens: _Optional[int] = ..., audio_tokens: _Optional[int] = ..., reasoning_tokens: _Optional[int] = ..., rejected_prediction_tokens: _Optional[int] = ...) -> None: ...

class PromptTokensDetails(_message.Message):
    __slots__ = ("audio_tokens", "cached_tokens")
    AUDIO_TOKENS_FIELD_NUMBER: _ClassVar[int]
    CACHED_TOKENS_FIELD_NUMBER: _ClassVar[int]
    audio_tokens: int
    cached_tokens: int
    def __init__(self, audio_tokens: _Optional[int] = ..., cached_tokens: _Optional[int] = ...) -> None: ...

class WebRetrievalRequest(_message.Message):
    __slots__ = ("uids", "search_query", "n_miners", "n_results", "max_response_time", "timeout")
    UIDS_FIELD_NUMBER: _ClassVar[int]
    SEARCH_QUERY_FIELD_NUMBER: _ClassVar[int]
    N_MINERS_FIELD_NUMBER: _ClassVar[int]
    N_RESULTS_FIELD_NUMBER: _ClassVar[int]
    MAX_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    uids: _containers.RepeatedScalarFieldContainer[int]
    search_query: str
    n_miners: int
    n_results: int
    max_response_time: int
    timeout: int
    def __init__(self, uids: _Optional[_Iterable[int]] = ..., search_query: _Optional[str] = ..., n_miners: _Optional[int] = ..., n_results: _Optional[int] = ..., max_response_time: _Optional[int] = ..., timeout: _Optional[int] = ...) -> None: ...

class WebSearchResult(_message.Message):
    __slots__ = ("url", "content", "relevant")
    URL_FIELD_NUMBER: _ClassVar[int]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    RELEVANT_FIELD_NUMBER: _ClassVar[int]
    url: str
    content: str
    relevant: str
    def __init__(self, url: _Optional[str] = ..., content: _Optional[str] = ..., relevant: _Optional[str] = ...) -> None: ...

class WebRetrievalResponse(_message.Message):
    __slots__ = ("results",)
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[WebSearchResult]
    def __init__(self, results: _Optional[_Iterable[_Union[WebSearchResult, _Mapping]]] = ...) -> None: ...

class SubmitDeepResearcherJobResponse(_message.Message):
    __slots__ = ("job_id", "status", "created_at", "updated_at")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: str
    created_at: str
    updated_at: str
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ...) -> None: ...

class GetDeepResearcherJobResponse(_message.Message):
    __slots__ = ("job_id", "status", "created_at", "updated_at", "result", "error")
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    status: str
    created_at: str
    updated_at: str
    result: _containers.RepeatedCompositeFieldContainer[DeepResearcherResultChunk]
    error: str
    def __init__(self, job_id: _Optional[str] = ..., status: _Optional[str] = ..., created_at: _Optional[str] = ..., updated_at: _Optional[str] = ..., result: _Optional[_Iterable[_Union[DeepResearcherResultChunk, _Mapping]]] = ..., error: _Optional[str] = ...) -> None: ...

class DeepResearcherResultChunk(_message.Message):
    __slots__ = ("seq_id", "chunk")
    SEQ_ID_FIELD_NUMBER: _ClassVar[int]
    CHUNK_FIELD_NUMBER: _ClassVar[int]
    seq_id: int
    chunk: str
    def __init__(self, seq_id: _Optional[int] = ..., chunk: _Optional[str] = ...) -> None: ...

class GetDeepResearcherJobRequest(_message.Message):
    __slots__ = ("job_id",)
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: str
    def __init__(self, job_id: _Optional[str] = ...) -> None: ...

class ChatSession(_message.Message):
    __slots__ = ("id", "user_id", "title", "chat_type", "created_at", "updated_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    USER_ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    UPDATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    user_id: str
    title: str
    chat_type: str
    created_at: _timestamp_pb2.Timestamp
    updated_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., user_id: _Optional[str] = ..., title: _Optional[str] = ..., chat_type: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., updated_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class GetChatSessionsResponse(_message.Message):
    __slots__ = ("chat_sessions",)
    CHAT_SESSIONS_FIELD_NUMBER: _ClassVar[int]
    chat_sessions: _containers.RepeatedCompositeFieldContainer[ChatSession]
    def __init__(self, chat_sessions: _Optional[_Iterable[_Union[ChatSession, _Mapping]]] = ...) -> None: ...

class GetStoredChatCompletionsRequest(_message.Message):
    __slots__ = ("chat_id",)
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    def __init__(self, chat_id: _Optional[str] = ...) -> None: ...

class StoredChatCompletion(_message.Message):
    __slots__ = ("id", "chat_id", "completion_type", "created_at", "completed_at", "user_prompt_text", "completion_text", "metadata", "error_message")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TYPE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    COMPLETED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_PROMPT_TEXT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    id: str
    chat_id: str
    completion_type: str
    created_at: _timestamp_pb2.Timestamp
    completed_at: _timestamp_pb2.Timestamp
    user_prompt_text: str
    completion_text: str
    metadata: _struct_pb2.Struct
    error_message: str
    def __init__(self, id: _Optional[str] = ..., chat_id: _Optional[str] = ..., completion_type: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., completed_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_prompt_text: _Optional[str] = ..., completion_text: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., error_message: _Optional[str] = ...) -> None: ...

class GetStoredChatCompletionsResponse(_message.Message):
    __slots__ = ("chat_completions",)
    CHAT_COMPLETIONS_FIELD_NUMBER: _ClassVar[int]
    chat_completions: _containers.RepeatedCompositeFieldContainer[StoredChatCompletion]
    def __init__(self, chat_completions: _Optional[_Iterable[_Union[StoredChatCompletion, _Mapping]]] = ...) -> None: ...

class UpdateChatAttributesRequest(_message.Message):
    __slots__ = ("chat_id", "attributes")
    class AttributesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    attributes: _containers.ScalarMap[str, str]
    def __init__(self, chat_id: _Optional[str] = ..., attributes: _Optional[_Mapping[str, str]] = ...) -> None: ...

class UpdateChatAttributesResponse(_message.Message):
    __slots__ = ("chat",)
    CHAT_FIELD_NUMBER: _ClassVar[int]
    chat: ChatSession
    def __init__(self, chat: _Optional[_Union[ChatSession, _Mapping]] = ...) -> None: ...

class DeleteChatsRequest(_message.Message):
    __slots__ = ("chat_ids",)
    CHAT_IDS_FIELD_NUMBER: _ClassVar[int]
    chat_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chat_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteChatsResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class ParsedChat(_message.Message):
    __slots__ = ("id", "title", "created_at", "chat_type")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: str
    title: str
    created_at: _timestamp_pb2.Timestamp
    chat_type: str
    def __init__(self, id: _Optional[str] = ..., title: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., chat_type: _Optional[str] = ...) -> None: ...

class ParsedCompletion(_message.Message):
    __slots__ = ("id", "chat_id", "created_at", "user_prompt_text", "completion_text", "completion_type", "metadata")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    USER_PROMPT_TEXT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TEXT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    id: str
    chat_id: str
    created_at: _timestamp_pb2.Timestamp
    user_prompt_text: str
    completion_text: str
    completion_type: str
    metadata: _struct_pb2.Struct
    def __init__(self, id: _Optional[str] = ..., chat_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., user_prompt_text: _Optional[str] = ..., completion_text: _Optional[str] = ..., completion_type: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class CreateChatAndCompletionRequest(_message.Message):
    __slots__ = ("user_prompt", "chat_type", "completion_type", "title")
    USER_PROMPT_FIELD_NUMBER: _ClassVar[int]
    CHAT_TYPE_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TYPE_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    user_prompt: str
    chat_type: str
    completion_type: str
    title: str
    def __init__(self, user_prompt: _Optional[str] = ..., chat_type: _Optional[str] = ..., completion_type: _Optional[str] = ..., title: _Optional[str] = ...) -> None: ...

class CreateChatAndCompletionResponse(_message.Message):
    __slots__ = ("parsed_chat", "parsed_completion")
    PARSED_CHAT_FIELD_NUMBER: _ClassVar[int]
    PARSED_COMPLETION_FIELD_NUMBER: _ClassVar[int]
    parsed_chat: ParsedChat
    parsed_completion: ParsedCompletion
    def __init__(self, parsed_chat: _Optional[_Union[ParsedChat, _Mapping]] = ..., parsed_completion: _Optional[_Union[ParsedCompletion, _Mapping]] = ...) -> None: ...

class CreateCompletionRequest(_message.Message):
    __slots__ = ("chat_id", "user_prompt", "completion_type")
    CHAT_ID_FIELD_NUMBER: _ClassVar[int]
    USER_PROMPT_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TYPE_FIELD_NUMBER: _ClassVar[int]
    chat_id: str
    user_prompt: str
    completion_type: str
    def __init__(self, chat_id: _Optional[str] = ..., user_prompt: _Optional[str] = ..., completion_type: _Optional[str] = ...) -> None: ...

class CreateCompletionResponse(_message.Message):
    __slots__ = ("parsed_completion",)
    PARSED_COMPLETION_FIELD_NUMBER: _ClassVar[int]
    parsed_completion: ParsedCompletion
    def __init__(self, parsed_completion: _Optional[_Union[ParsedCompletion, _Mapping]] = ...) -> None: ...

class DeleteCompletionsRequest(_message.Message):
    __slots__ = ("completion_ids",)
    COMPLETION_IDS_FIELD_NUMBER: _ClassVar[int]
    completion_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, completion_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteCompletionsResponse(_message.Message):
    __slots__ = ("success",)
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...

class SearchChatIdsByPromptAndCompletionTextRequest(_message.Message):
    __slots__ = ("search_term",)
    SEARCH_TERM_FIELD_NUMBER: _ClassVar[int]
    search_term: str
    def __init__(self, search_term: _Optional[str] = ...) -> None: ...

class SearchChatIdsByPromptAndCompletionTextResponse(_message.Message):
    __slots__ = ("chat_ids",)
    CHAT_IDS_FIELD_NUMBER: _ClassVar[int]
    chat_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, chat_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class UpdateCompletionAttributesRequest(_message.Message):
    __slots__ = ("completion_id", "completion_text", "metadata")
    COMPLETION_ID_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_TEXT_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    completion_id: str
    completion_text: str
    metadata: _struct_pb2.Struct
    def __init__(self, completion_id: _Optional[str] = ..., completion_text: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class UpdateCompletionAttributesResponse(_message.Message):
    __slots__ = ("completion",)
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    completion: StoredChatCompletion
    def __init__(self, completion: _Optional[_Union[StoredChatCompletion, _Mapping]] = ...) -> None: ...

class GetCompletionsWithDeepResearcherEntryResponse(_message.Message):
    __slots__ = ("completions",)
    COMPLETIONS_FIELD_NUMBER: _ClassVar[int]
    completions: _containers.RepeatedCompositeFieldContainer[ParsedCompletion]
    def __init__(self, completions: _Optional[_Iterable[_Union[ParsedCompletion, _Mapping]]] = ...) -> None: ...
