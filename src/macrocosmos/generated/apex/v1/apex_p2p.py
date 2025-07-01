# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.3.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.5 
# Pydantic Version: 2.11.7 
from datetime import datetime
from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel
from pydantic import Field
import typing


class ChatMessage(BaseModel):
    """
     The choice object for the chunk.
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# role: the role of the message.
    role: str = Field(default="")
# content: the content of the message.
    content: str = Field(default="")

class SamplingParameters(BaseModel):
    """
     The sampling parameters for the completion.
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# temperature: the temperature to use for the completion.
    temperature: float = Field(default=0.0)
# top_p: the top_p to use for the completion.
    top_p: float = Field(default=0.0)
# top_k: the top_k to use for the completion.
    top_k: typing.Optional[float] = Field(default=0.0)
# max_new_tokens: the max_new_tokens to use for the completion.
    max_new_tokens: int = Field(default=0)
# do_sample: whether to do sample for the completion.
    do_sample: bool = Field(default=False)

class ChatCompletionRequest(BaseModel):
    """
     A request to generate completions following Apex CompletionsRequest format.
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# uids: the miner UIDs that will be used to generate the completion (optional).
    uids: typing.List[int] = Field(default_factory=list)
# messages: the messages to generate completions for.
    messages: typing.List[ChatMessage] = Field(default_factory=list)
# seed: the seed to use for the completion.
    seed: typing.Optional[int] = Field(default=0)
# task: the task to generate completions for (e.g. "InferenceTask").
    task: typing.Optional[str] = Field(default="")
# model: the LLM name to use for the completion. (optional, suggest leaving this empty as not all LLMs are supported)
    model: typing.Optional[str] = Field(default="")
# test_time_inference: whether to use test time inference.
    test_time_inference: typing.Optional[bool] = Field(default=False)
# mixture: whether to use a mixture of miners to create a slower but better answer.
    mixture: typing.Optional[bool] = Field(default=False)
# sampling_parameters: the sampling parameters to use for the completion.
    sampling_parameters: typing.Optional[SamplingParameters] = Field(default_factory=SamplingParameters)
# inference_mode: the inference mode to use for the completion.
    inference_mode: typing.Optional[str] = Field(default="")
# json_format: whether to use JSON format for the completion.
    json_format: typing.Optional[bool] = Field(default=False)
# stream: whether to stream the completion.
    stream: typing.Optional[bool] = Field(default=False)
# timeout: the timeout for the completion in seconds.
    timeout: typing.Optional[int] = Field(default=0)

class TopLogprob(BaseModel):
    """
     The top logprob object for the token. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_token_logprob.py
    """

# token: the token of the logprob.
    token: str = Field(default="")
# bytes: the bytes of the logprob.
    bytes: typing.List[int] = Field(default_factory=list)
# logprob: the logprob of the token.
    logprob: float = Field(default=0.0)

class ChatCompletionTokenLogprob(BaseModel):
    """
     The chat completion token logprob object. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_token_logprob.py
    """

# token: the token of the logprob.
    token: str = Field(default="")
# bytes: the bytes of the logprob.
    bytes: typing.List[int] = Field(default_factory=list)
# logprob: the logprob of the token.
    logprob: float = Field(default=0.0)
# top_logprobs: the top logprobs of the token.
    top_logprobs: typing.List[TopLogprob] = Field(default_factory=list)

class ChoiceLogprobs(BaseModel):
    """
     The logprobs object for the choice.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# content: the content of the logprobs.
    content: typing.List[ChatCompletionTokenLogprob] = Field(default_factory=list)
# refusal: the refusal of the logprobs.
    refusal: typing.List[ChatCompletionTokenLogprob] = Field(default_factory=list)

class Annotation(BaseModel):
    """
     The annotation object for the message. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_message.py
    """

# content: the content of the annotation.
    content: str = Field(default="")
# role: the role of the annotation.
    role: str = Field(default="")

class ChatCompletionAudio(BaseModel):
    """
     The audio object for the message. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_audio.py
    """

# id: the id of the audio.
    id: str = Field(default="")
# data: the data of the audio.
    data: str = Field(default="")
# expires_at: the expires at of the audio.
    expires_at: int = Field(default=0)
# transcript: the transcript of the audio.
    transcript: str = Field(default="")

class FunctionCall(BaseModel):
    """
     The function call object for the message.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_message.py
    """

# arguments: the arguments of the function call.
    arguments: typing.List[str] = Field(default_factory=list)
# name: the name of the function call.
    name: str = Field(default="")

class Function(BaseModel):
    """
     The function object for the tool call.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_message_tool_call.py
    """

# arguments: the arguments of the function.
    arguments: typing.List[str] = Field(default_factory=list)
# name: the name of the function.
    name: str = Field(default="")

class ChatCompletionMessageToolCall(BaseModel):
    """
     The tool call object for the message.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_message_tool_call.py
    """

# id: the id of the tool call.
    id: str = Field(default="")
# function: the function object for the tool call.
    function: Function = Field(default_factory=Function)
# type: the type of the tool call.
    type: str = Field(default="")

class ChatCompletionMessage(BaseModel):
    """
     The message response object from the LLM.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_message.py
    """

# content: the content of the message.
    content: str = Field(default="")
# refusal: the refusal of the message. (not currently supported in Apex)
    refusal: str = Field(default="")
# role: the role of the message.
    role: str = Field(default="")
# annotations: the annotations of the message. (not currently supported in Apex)
    annotations: typing.List[Annotation] = Field(default_factory=list)
# audio: the audio of the message. (not currently supported in Apex)
    audio: ChatCompletionAudio = Field(default_factory=ChatCompletionAudio)
# function_call: the function call of the message.
    function_call: FunctionCall = Field(default_factory=FunctionCall)
# tool_calls: the tool calls of the message.
    tool_calls: typing.List[ChatCompletionMessageToolCall] = Field(default_factory=list)

class Choice(BaseModel):
    """
     The choice object containing the message response from the LLM for the completion.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion.py
    """

# finish_reason: the finish reason of the choice.
    finish_reason: str = Field(default="")
# index: the index of the choice.
    index: int = Field(default=0)
# logprobs: the logprobs of the choice.
    logprobs: ChoiceLogprobs = Field(default_factory=ChoiceLogprobs)
# message: the message of the choice.
    message: ChatCompletionMessage = Field(default_factory=ChatCompletionMessage)

class CompletionTokensDetails(BaseModel):
    """
     The completion tokens details object. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/completion_usage.py
    """

# accepted_prediction_tokens: the accepted prediction tokens of the details.
    accepted_prediction_tokens: int = Field(default=0)
# audio_tokens: the audio tokens of the details.
    audio_tokens: int = Field(default=0)
# reasoning_tokens: the reasoning tokens of the details.
    reasoning_tokens: int = Field(default=0)
# rejected_prediction_tokens: the rejected prediction tokens of the details.
    rejected_prediction_tokens: int = Field(default=0)

class PromptTokensDetails(BaseModel):
    """
     The prompt tokens details object. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/completion_usage.py
    """

# audio_tokens: the audio tokens of the details.
    audio_tokens: int = Field(default=0)
# cached_tokens: the cached tokens of the details.
    cached_tokens: int = Field(default=0)

class CompletionUsage(BaseModel):
    """
     The completion usage object. (not currently supported in Apex)
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/completion_usage.py
    """

# completion_tokens: the completion tokens of the usage.
    completion_tokens: int = Field(default=0)
# prompt_tokens: the prompt tokens of the usage.
    prompt_tokens: int = Field(default=0)
# total_tokens: the total tokens of the usage.
    total_tokens: int = Field(default=0)
# completion_tokens_details: the completion tokens details of the usage.
    completion_tokens_details: CompletionTokensDetails = Field(default_factory=CompletionTokensDetails)
# prompt_tokens_details: the prompt tokens details of the usage.
    prompt_tokens_details: PromptTokensDetails = Field(default_factory=PromptTokensDetails)

class ChatCompletionResponse(BaseModel):
    """
     A chat completion response, following OpenAI's ChatCompletion format.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion.py
    """

# id: the id of the completion.
    id: str = Field(default="")
# choices: the choices of the completion.
    choices: typing.List[Choice] = Field(default_factory=list)
# created: the created time of the completion.
    created: int = Field(default=0)
# model: the model of the completion.
    model: str = Field(default="")
# object: the object of the completion.
    object: str = Field(default="")
# service_tier: the service tier of the completion. (not currently supported in Apex)
    service_tier: str = Field(default="")
# system_fingerprint: the system fingerprint of the completion. (not currently supported in Apex)
    system_fingerprint: str = Field(default="")
# usage: the usage of the completion. (not currently supported in Apex)
    usage: CompletionUsage = Field(default_factory=CompletionUsage)

class ChoiceDeltaFunctionCall(BaseModel):
    """
     The function call object for the delta.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# arguments: the arguments of the function call.
    arguments: typing.List[str] = Field(default_factory=list)
# name: the name of the function call.
    name: str = Field(default="")

class ChoiceDeltaToolCallFunction(BaseModel):
    """
     The function object for the tool call.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# arguments: the arguments of the function.
    arguments: typing.List[str] = Field(default_factory=list)
# name: the name of the function.
    name: str = Field(default="")

class ChoiceDeltaToolCall(BaseModel):
    """
     The tool call object for the delta.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# index: the index of the tool call.
    index: int = Field(default=0)
# id: the id of the tool call.
    id: str = Field(default="")
# function: the function object for the tool call.
    function: ChoiceDeltaToolCallFunction = Field(default_factory=ChoiceDeltaToolCallFunction)
# type: the type of the tool call.
    type: str = Field(default="")

class ChoiceDelta(BaseModel):
    """
     The delta object for the choice.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# content: the content of the delta.
    content: str = Field(default="")
# function_call: the function call of the delta.
    function_call: ChoiceDeltaFunctionCall = Field(default_factory=ChoiceDeltaFunctionCall)
# refusal: the refusal of the delta.
    refusal: str = Field(default="")
# role: the role of the delta.
    role: str = Field(default="")
# tool_calls: the tool calls of the delta.
    tool_calls: typing.List[ChoiceDeltaToolCall] = Field(default_factory=list)

class ChunkChoice(BaseModel):
    """
     The choice object for the chunk.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# delta: the delta of the choice.
    delta: ChoiceDelta = Field(default_factory=ChoiceDelta)
# finish_reason: the finish reason of the choice.
    finish_reason: str = Field(default="")
# index: the index of the choice.
    index: int = Field(default=0)
# logprobs: the logprobs of the choice. (not currently supported in Apex)
    logprobs: ChoiceLogprobs = Field(default_factory=ChoiceLogprobs)

class ChatCompletionChunkResponse(BaseModel):
    """
     A streaming chunk response, following OpenAI's ChatCompletionChunk format.
 Parsed from https://github.com/openai/openai-python/blob/main/src/openai/types/chat/chat_completion_chunk.py
    """

# id: the id of the chunk.
    id: str = Field(default="")
# choices: the choices of the chunk.
    choices: typing.List[ChunkChoice] = Field(default_factory=list)
# created: the created time of the chunk.
    created: int = Field(default=0)
# model: the model of the chunk.
    model: str = Field(default="")
# object: the object of the chunk. (not currently supported in Apex)
    object: str = Field(default="")
# service_tier: the service tier of the chunk. (not currently supported in Apex)
    service_tier: str = Field(default="")
# system_fingerprint: the system fingerprint of the chunk. (not currently supported in Apex)
    system_fingerprint: str = Field(default="")
# usage: the usage of the chunk. (not currently supported in Apex)
    usage: CompletionUsage = Field(default_factory=CompletionUsage)

class WebRetrievalRequest(BaseModel):
    """
     A web retrieval request from Apex
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# uids: the miner UIDs that will be used to generate the completion (optional).
    uids: typing.List[int] = Field(default_factory=list)
# search_query: the search query.
    search_query: str = Field(default="")
# n_miners: the number of miners to use for the query.
    n_miners: typing.Optional[int] = Field(default=0)
# n_results: the number of results to return.
    n_results: typing.Optional[int] = Field(default=0)
# max_response_time: the max response time to allow for the miners to respond in seconds.
    max_response_time: typing.Optional[int] = Field(default=0)
# timeout: the timeout for the web retrieval in seconds.
    timeout: typing.Optional[int] = Field(default=0)

class WebSearchResult(BaseModel):
    """
     A web search result from Apex
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# url: the url of the result.
    url: str = Field(default="")
# content: the entire page contents.
    content: str = Field(default="")
# relevant: the relevant part of the page best fitting the query..
    relevant: str = Field(default="")

class WebRetrievalResponse(BaseModel):
    """
     A web retrieval response from Apex
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# results: the results of the web retrieval.
    results: typing.List[WebSearchResult] = Field(default_factory=list)

class SubmitDeepResearcherJobResponse(BaseModel):
    """
     A response containing the deep researcher job submission details
    """

# job_id: unique identifier for the submitted job
    job_id: str = Field(default="")
# status: current status of the job
    status: str = Field(default="")
# created_at: timestamp when the job was created
    created_at: str = Field(default="")
# updated_at: timestamp when the job was last updated
    updated_at: str = Field(default="")

class DeepResearcherResultChunk(BaseModel):
    """
     A chunk of the deep researcher result
    """

# seq_id: sequence identifier for the chunk
    seq_id: int = Field(default=0)
# chunk: the content of the chunk
    chunk: str = Field(default="")

class GetDeepResearcherJobResponse(BaseModel):
    """
     A response containing the deep researcher job status and results
    """

# job_id: unique identifier for the job
    job_id: str = Field(default="")
# status: current status of the job
    status: str = Field(default="")
# created_at: timestamp when the job was created
    created_at: str = Field(default="")
# updated_at: timestamp when the job was last updated
    updated_at: str = Field(default="")
# result: array of result chunks
    result: typing.List[DeepResearcherResultChunk] = Field(default_factory=list)
# error: error message if the job failed
    error: typing.Optional[str] = Field(default="")

class GetDeepResearcherJobRequest(BaseModel):
    """
     A request to get the status of a deep researcher job
    """

# job_id: the ID of the job to retrieve
    job_id: str = Field(default="")

class ChatSession(BaseModel):
    """
     A GetChatSession message repeated in GetChatSessionsResponse
    """

# id: chat id
    id: str = Field(default="")
# user_id: user id
    user_id: str = Field(default="")
# title: title of chat
    title: str = Field(default="")
# chat_type: e.g. apex
    chat_type: str = Field(default="")
# created_at: when the chat was created
    created_at: datetime = Field(default_factory=datetime.now)
# updated_at: when the chat was updated
    updated_at: datetime = Field(default_factory=datetime.now)

class GetChatSessionsResponse(BaseModel):
    """
     A GetChatSessionsResponse response
    """

# chat_sessions: the chat sessions
    chat_sessions: typing.List[ChatSession] = Field(default_factory=list)

class GetStoredChatCompletionsRequest(BaseModel):
    """
     A GetStoredChatCompletionRequest request message
    """

# chat_id: a unique identifier for a chat
    chat_id: str = Field(default="")

class StoredChatCompletion(BaseModel):
    """
     A StoredChatCompletion message repeated in GetStoredChatCompletionsResponse
    """

# id: chat completion id
    id: str = Field(default="")
# chat_id: chat id
    chat_id: str = Field(default="")
# completion_type: type of completion
    completion_type: str = Field(default="")
# created_at: when the chat was created
    created_at: datetime = Field(default_factory=datetime.now)
# completed_at: when the chat was updated
    completed_at: datetime = Field(default_factory=datetime.now)
# user_prompt_text: user_prompt_text of chat
    user_prompt_text: str = Field(default="")
# completion_text: completion_text of chat
    completion_text: str = Field(default="")
# metadata: metadata json blob
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)
# error_message: error_message if any
    error_message: str = Field(default="")

class GetStoredChatCompletionsResponse(BaseModel):
    """
     A GetChatStoredChatCompletionResponse response
    """

# chat_completions: the chat completions
    chat_completions: typing.List[StoredChatCompletion] = Field(default_factory=list)

class UpdateChatAttributesRequest(BaseModel):
    """
     Directly model the attributes as a map
    """

# chat_id: the unique id associated to a users chat message
    chat_id: str = Field(default="")
# attributes: the data attributes captured in the chat logging process
    attributes: "typing.Dict[str, str]" = Field(default_factory=dict)

class UpdateChatAttributesResponse(BaseModel):
    """
     A UpdateChatAttributes response
    """

# chat: the updated chat row from the chats table
    chat: ChatSession = Field(default_factory=ChatSession)

class DeleteChatsRequest(BaseModel):
    """
     A DeleteChats request
    """

# chat_ids: the unique ids associated to user chat messages that should be deleted
    chat_ids: typing.List[str] = Field(default_factory=list)

class DeleteChatsResponse(BaseModel):
    """
     A DeleteChats response
    """

# success: indicates if the deletion was successful
    success: bool = Field(default=False)

class ParsedChat(BaseModel):
    """
     A ParsedChat message serving as part of the CreateChatAndCompletion response
    """

# id: the chat_id
    id: str = Field(default="")
# title: title of the chat
    title: str = Field(default="")
# created_at: the time the chat was created
    created_at: datetime = Field(default_factory=datetime.now)
# chat_type: the service a single chat can be using (e.g.: "apex", "gravity")
    chat_type: str = Field(default="")

class ParsedCompletion(BaseModel):
    """
     A ParsedCompletion message serving as part of the CreateChatAndCompletion response
    """

# id: the completion_id
    id: str = Field(default="")
#chat_id: the chat_id
    chat_id: str = Field(default="")
# created_at: the time the completion was created
    created_at: datetime = Field(default_factory=datetime.now)
# user_prompt_text: the user's chat prompt text
    user_prompt_text: str = Field(default="")
# completion_text: the user's completion text 
    completion_text: str = Field(default="")
# completion_type: type of completion
    completion_type: str = Field(default="")
# metadata: metadata json blob
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)

class CreateChatAndCompletionRequest(BaseModel):
    """
     A CreateChatAndCompletion request
    """

# user_prompt: the prompt the user issues
    user_prompt: str = Field(default="")
# chat_type: the service a single chat can be using (e.g.: "apex", "gravity")
    chat_type: str = Field(default="")
# completion_type: specific to completions and might accompany specific kinds of metadata (e.g.: "basic", "combined")
    completion_type: str = Field(default="")
# title: the title of the new chat (optional)
    title: typing.Optional[str] = Field(default="")

class CreateChatAndCompletionResponse(BaseModel):
    """
     A CreateChatAndCompletion response
    """

# parsed_chat: the chat row that was successfully created
    parsed_chat: ParsedChat = Field(default_factory=ParsedChat)
# parsed_completion: the completion row that was successfully created
    parsed_completion: ParsedCompletion = Field(default_factory=ParsedCompletion)

class CreateCompletionRequest(BaseModel):
    """
     A CreateCompletion request
    """

# chat_id: the ID of the chat to create the completion for
    chat_id: str = Field(default="")
# user_prompt: the prompt the user issues
    user_prompt: str = Field(default="")
# completion_type: the completion type e.g. basic, reasoning etc.
    completion_type: str = Field(default="")

class CreateCompletionResponse(BaseModel):
    """
     A CreateCompletion response
    """

# parsed_completion: the completion row that was successfully created
    parsed_completion: ParsedCompletion = Field(default_factory=ParsedCompletion)

class DeleteCompletionsRequest(BaseModel):
    """
     A DeleteCompletions request
    """

# completion_ids: the unique ids associated to user chat-completions that should be deleted
    completion_ids: typing.List[str] = Field(default_factory=list)

class DeleteCompletionsResponse(BaseModel):
    """
     A DeleteCompletions response
    """

# success: indicates if the deletion was successful
    success: bool = Field(default=False)

class SearchChatIdsByPromptAndCompletionTextRequest(BaseModel):
    """
     A SearchChatIdsByPromptAndCompletionText request
    """

# search_term: the user supplied search term
    search_term: str = Field(default="")

class SearchChatIdsByPromptAndCompletionTextResponse(BaseModel):
    """
     A SearchChatIdsByPromptAndCompletionText response
    """

# chat_ids: a list of chat_ids which adhere to the search criteria
    chat_ids: typing.List[str] = Field(default_factory=list)

class UpdateCompletionAttributesRequest(BaseModel):
    """
     An UpdateCompletionAttributes request
    """

# completion_id: the chat completion id
    completion_id: str = Field(default="")
# completion_text: the user's completion text (optional)
    completion_text: typing.Optional[str] = Field(default="")
# metadata: metadata json blob (optional)
    metadata: typing.Dict[str, typing.Any] = Field(default_factory=dict)

class UpdateCompletionAttributesResponse(BaseModel):
    """
     An UpdateCompletionAttributes response
    """

# completion: the chat completion that has been updated
    completion: StoredChatCompletion = Field(default_factory=StoredChatCompletion)

class GetCompletionsWithDeepResearcherEntryResponse(BaseModel):
    """
     A GetCompletionsWithDeepResearcherEntry response (request is not required)
    """

# completions: a list of completion objects containing deep researcher metadata
    completions: typing.List[ParsedCompletion] = Field(default_factory=list)
