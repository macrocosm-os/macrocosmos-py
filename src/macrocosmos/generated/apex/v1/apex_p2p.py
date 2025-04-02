# This is an automatically generated file, please do not change
# gen by protobuf_to_pydantic[v0.3.1.1](https://github.com/so1n/protobuf_to_pydantic)
# Protobuf Version: 5.29.4 
# Pydantic Version: 2.11.0 
import typing

from google.protobuf.message import Message  # type: ignore
from pydantic import BaseModel, Field


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
    top_k: float = Field(default=0.0)
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
    seed: int = Field(default=0)
# task: the task to generate completions for (e.g. "InferenceTask").
    task: str = Field(default="")
# model: the LLM name to use for the completion. (optional, suggest leaving this empty as not all LLMs are supported)
    model: str = Field(default="")
# test_time_inference: whether to use test time inference.
    test_time_inference: bool = Field(default=False)
# mixture: whether to use a mixture of miners to create a slower but better answer.
    mixture: bool = Field(default=False)
# sampling_parameters: the sampling parameters to use for the completion.
    sampling_parameters: SamplingParameters = Field(default_factory=SamplingParameters)
# inference_mode: the inference mode to use for the completion.
    inference_mode: str = Field(default="")
# json_format: whether to use JSON format for the completion.
    json_format: bool = Field(default=False)
# stream: whether to stream the completion.
    stream: bool = Field(default=False)

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
     A web retrival request from Apex
 Parsed from https://github.com/macrocosm-os/prompting/blob/main/validator_api/serializers.py
    """

# uids: the miner UIDs that will be used to generate the completion (optional).
    uids: typing.List[int] = Field(default_factory=list)
# search_query: the search query.
    search_query: str = Field(default="")
# n_miners: the number of miners to use for the query.
    n_miners: int = Field(default=0)
# n_results: the number of results to return.
    n_results: int = Field(default=0)
# max_response_time: the max response time to allow for the miners to respond in seconds.
    max_response_time: int = Field(default=0)

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
