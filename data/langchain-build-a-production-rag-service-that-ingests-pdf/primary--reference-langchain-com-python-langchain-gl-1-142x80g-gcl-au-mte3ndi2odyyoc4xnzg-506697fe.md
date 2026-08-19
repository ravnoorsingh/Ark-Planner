---
library: "langchain"
query: "Build a production RAG service that ingests PDF manuals, chunks and embeds them into a vector database, and exposes a FastAPI endpoint that answers questions with citations back to the source page. Use pypdf for extraction and Pydantic models for request and response validation. Include streaming responses and health checks. Use pymilvus for the vector database."
url: "https://reference.langchain.com/python/langchain?_gl=1*142x80g*_gcl_au*MTE3NDI2ODYyOC4xNzg2MDA3OTI4*_ga*MjA0NjkxODk3MC4xNzg1NzgyMDcy*_ga_47WX3HKKY2*czE3ODcxNDI2NzMkbzE5JGcxJHQxNzg3MTQyNzE4JGoxNSRsMCRoMA.."
role: "primary"
rank: 0
fetched_at: "2026-08-19T12:36:07.352014+00:00"
fetched_via: "brightdata-collector:c_msx9i6aq2bz5dznadk"
sha256: "258a877031343dbf67a7f5dd44fda82a852f9a218e82d5cb1a9ef61e5fe02bca"
---

# langchain

## Description

# 🦜️🔗 LangChain

[![PyPI - Version](https://img.shields.io/pypi/v/langchain?label=%20)](https://pypi.org/project/langchain/#history)   [![PyPI - License](https://img.shields.io/pypi/l/langchain)](https://opensource.org/licenses/MIT)   [![PyPI - Downloads](https://img.shields.io/pepy/dt/langchain)](https://pypistats.org/packages/langchain)   [![Twitter](https://img.shields.io/twitter/url/https/twitter.com/langchain_oss.svg?style=social&label=Follow%20%40LangChain)](https://x.com/langchain_oss)

Looking for the JS/TS version? Check out [LangChain.js](https://github.com/langchain-ai/langchainjs) .

To help you ship LangChain apps to production faster, check out [LangSmith](https://www.langchain.com/langsmith) . [LangSmith](https://www.langchain.com/langsmith) is a unified developer platform for building, testing, and monitoring LLM applications.

## Quick Install

```
uv add langchain
```

Copy

## 🤔 What is this?

LangChain is the easiest way to start building agents and applications powered by LLMs. With under 10 lines of code, you can connect to OpenAI, Anthropic, Google, and [more](https://docs.langchain.com/oss/python/integrations/providers/overview) . LangChain provides a pre-built agent architecture and model integrations to help you get started quickly and seamlessly incorporate LLMs into your agents and applications.

We recommend you use LangChain if you want to quickly build agents and autonomous applications. Use [LangGraph](https://docs.langchain.com/oss/python/langgraph/overview) , our low-level agent orchestration framework and runtime, when you have more advanced needs that require a combination of deterministic and agentic workflows, heavy customization, and carefully controlled latency.

LangChain [agents](https://docs.langchain.com/oss/python/langchain/agents) are built on top of LangGraph in order to provide durable execution, streaming, human-in-the-loop, persistence, and more. (You do not need to know LangGraph for basic LangChain agent usage.)

## 📖 Documentation

For full documentation, see the [API reference](https://reference.langchain.com/python/langchain/langchain/) . For conceptual guides, tutorials, and examples on using LangChain, see the [LangChain Docs](https://docs.langchain.com/oss/python/langchain/overview) . You can also chat with the docs using [Chat LangChain](https://chat.langchain.com) .

## 📕 Releases & Versioning

See our [Releases](https://docs.langchain.com/oss/python/release-policy) and [Versioning](https://docs.langchain.com/oss/python/versioning) policies.

## 💁 Contributing

As an open-source project in a rapidly developing field, we are extremely open to contributions, whether it be in the form of a new feature, improved infrastructure, or better documentation.

For detailed information on how to contribute, see the [Contributing Guide](https://docs.langchain.com/oss/python/contributing/overview) .

## Resources

* [LangChain Academy](https://academy.langchain.com/) — comprehensive, free courses on LangChain libraries and products, made by the LangChain team
* [Code of Conduct](https://github.com/langchain-ai/langchain/?tab=coc-ov-file) — community guidelines and standards

## Classes

[Class

### SubagentRunStream

Typed sync handle for a nested named-agent execution.](/python/langchain/agents/_subagent_transformer/SubagentRunStream) [Class

### AsyncSubagentRunStream

Typed async handle for a nested named-agent execution.](/python/langchain/agents/_subagent_transformer/AsyncSubagentRunStream) [Class

### SubagentTransformer

Promote nested named agents into typed handles on `run.subagents` .](/python/langchain/agents/_subagent_transformer/SubagentTransformer) [Class

### StructuredOutputError

Base class for structured output errors.](/python/langchain/agents/structured_output/StructuredOutputError) [Class

### MultipleStructuredOutputsError

Raised when model returns multiple structured output tool calls when only one is expected.](/python/langchain/agents/structured_output/MultipleStructuredOutputsError) [Class

### StructuredOutputValidationError

Raised when structured output tool call arguments fail to parse according to the schema.](/python/langchain/agents/structured_output/StructuredOutputValidationError) [Class

### ToolStrategy

Use a tool calling strategy for model responses.](/python/langchain/agents/structured_output/ToolStrategy) [Class

### ProviderStrategy

Use the model provider's native structured output method.](/python/langchain/agents/structured_output/ProviderStrategy) [Class

### OutputToolBinding

Information for tracking structured output tool metadata.](/python/langchain/agents/structured_output/OutputToolBinding) [Class

### ProviderStrategyBinding

Information for tracking native structured output metadata.](/python/langchain/agents/structured_output/ProviderStrategyBinding) [Class

### AutoStrategy

Automatically select the best strategy for structured output.](/python/langchain/agents/structured_output/AutoStrategy) [Class

### ToolRetryMiddleware

Middleware that automatically retries failed tool calls with configurable backoff.](/python/langchain/agents/middleware/tool_retry/ToolRetryMiddleware) [Class

### ToolCallLimitState

State schema for `ToolCallLimitMiddleware` .](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitState) [Class

### ToolCallLimitExceededError

Exception raised when tool call limits are exceeded.](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitExceededError) [Class

### ToolCallLimitMiddleware

Track tool call counts and enforces limits during agent execution.](/python/langchain/agents/middleware/tool_call_limit/ToolCallLimitMiddleware) [Class

### ContextEdit

Protocol describing a context editing strategy.](/python/langchain/agents/middleware/context_editing/ContextEdit) [Class

### ClearToolUsesEdit

Configuration for clearing tool outputs when token limits are exceeded.](/python/langchain/agents/middleware/context_editing/ClearToolUsesEdit) [Class

### ContextEditingMiddleware

Automatically prune tool results to manage context size.](/python/langchain/agents/middleware/context_editing/ContextEditingMiddleware) [Class

### ShellToolState

Agent state extension for tracking shell session resources.](/python/langchain/agents/middleware/shell_tool/ShellToolState) [Class

### CommandExecutionResult

Structured result from command execution.](/python/langchain/agents/middleware/shell_tool/CommandExecutionResult) [Class

### ShellSession

Persistent shell session that supports sequential command execution.](/python/langchain/agents/middleware/shell_tool/ShellSession) [Class

### ShellToolMiddleware

Middleware that registers a persistent shell tool for agents.](/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware) [Class

### PIIMatch

Represents an individual match of sensitive data.](/python/langchain/agents/middleware/_redaction/PIIMatch) [Class

### PIIDetectionError

Raised when configured to block on detected sensitive values.](/python/langchain/agents/middleware/_redaction/PIIDetectionError) [Class

### RedactionRule

Configuration for handling a single PII type.](/python/langchain/agents/middleware/_redaction/RedactionRule) [Class

### ResolvedRedactionRule

Resolved redaction rule ready for execution.](/python/langchain/agents/middleware/_redaction/ResolvedRedactionRule) [Class

### LLMToolSelectorMiddleware

Uses an LLM to select relevant tools before calling the main model.](/python/langchain/agents/middleware/tool_selection/LLMToolSelectorMiddleware) [Class

### Todo

A single todo item with content and status.](/python/langchain/agents/middleware/todo/Todo) [Class

### PlanningState

State schema for the todo middleware.](/python/langchain/agents/middleware/todo/PlanningState) [Class

### WriteTodosInput

Input schema for the `write_todos` tool.](/python/langchain/agents/middleware/todo/WriteTodosInput) [Class

### TodoListMiddleware

Middleware that provides todo list management capabilities to agents.](/python/langchain/agents/middleware/todo/TodoListMiddleware) [Class

### ModelCallLimitState

State schema for `ModelCallLimitMiddleware` .](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitState) [Class

### ModelCallLimitExceededError

Exception raised when model call limits are exceeded.](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitExceededError) [Class

### ModelCallLimitMiddleware

Tracks model call counts and enforces limits.](/python/langchain/agents/middleware/model_call_limit/ModelCallLimitMiddleware) [Class

### FilesystemFileSearchMiddleware

Provides Glob and Grep search over filesystem files.](/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware) [Class

### ProviderToolSearchMiddleware

Defer selected tools behind provider-native tool search.](/python/langchain/agents/middleware/provider_tool_search/ProviderToolSearchMiddleware) [Class

### PIIMiddleware

Detect and handle Personally Identifiable Information (PII) in conversations.](/python/langchain/agents/middleware/pii/PIIMiddleware) [Class

### ModelRequest

Model request information for the agent.](/python/langchain/agents/middleware/types/ModelRequest) [Class

### ModelResponse

Response from model execution including messages and optional structured output.](/python/langchain/agents/middleware/types/ModelResponse) [Class

### ExtendedModelResponse

Model response with an optional 'Command' from 'wrap\_model\_call' middleware.](/python/langchain/agents/middleware/types/ExtendedModelResponse) [Class

### OmitFromSchema

Annotation used to mark state attributes as omitted from input or output schemas.](/python/langchain/agents/middleware/types/OmitFromSchema) [Class

### AgentState

State schema for the agent.](/python/langchain/agents/middleware/types/AgentState) [Class

### InputAgentState

Input state schema for the agent.](/python/langchain/agents/middleware/types/InputAgentState) [Class

### OutputAgentState

Output state schema for the agent.](/python/langchain/agents/middleware/types/OutputAgentState) [Class

### AgentMiddleware

Base middleware class for an agent.](/python/langchain/agents/middleware/types/AgentMiddleware) [Class

### Action

Represents an action with a name and args.](/python/langchain/agents/middleware/human_in_the_loop/Action) [Class

### ActionRequest

Represents an action request with a name, args, and description.](/python/langchain/agents/middleware/human_in_the_loop/ActionRequest) [Class

### ReviewConfig

Policy for reviewing a HITL request.](/python/langchain/agents/middleware/human_in_the_loop/ReviewConfig) [Class

### HITLRequest

Request for human feedback on a sequence of actions requested by a model.](/python/langchain/agents/middleware/human_in_the_loop/HITLRequest) [Class

### ApproveDecision

Response when a human approves the action.](/python/langchain/agents/middleware/human_in_the_loop/ApproveDecision) [Class

### EditDecision

Response when a human edits the action.](/python/langchain/agents/middleware/human_in_the_loop/EditDecision) [Class

### RejectDecision

Response when a human rejects the action.](/python/langchain/agents/middleware/human_in_the_loop/RejectDecision) [Class

### RespondDecision

Response when a human answers on behalf of the tool, skipping execution.](/python/langchain/agents/middleware/human_in_the_loop/RespondDecision) [Class

### HITLResponse

Response payload for a HITLRequest.](/python/langchain/agents/middleware/human_in_the_loop/HITLResponse) [Class

### InterruptOnConfig

Configuration for an action requiring human in the loop.](/python/langchain/agents/middleware/human_in_the_loop/InterruptOnConfig) [Class

### HumanInTheLoopMiddleware

Human in the loop middleware.](/python/langchain/agents/middleware/human_in_the_loop/HumanInTheLoopMiddleware) [Class

### BaseExecutionPolicy

Configuration contract for persistent shell sessions.](/python/langchain/agents/middleware/_execution/BaseExecutionPolicy) [Class

### HostExecutionPolicy

Run the shell directly on the host process.](/python/langchain/agents/middleware/_execution/HostExecutionPolicy) [Class

### CodexSandboxExecutionPolicy

Launch the shell through the Codex CLI sandbox.](/python/langchain/agents/middleware/_execution/CodexSandboxExecutionPolicy) [Class

### DockerExecutionPolicy

Run the shell inside a dedicated Docker container.](/python/langchain/agents/middleware/_execution/DockerExecutionPolicy) [Class

### ToolErrorMiddleware

Return selected tool-execution exceptions to the model as error `ToolMessage` s.](/python/langchain/agents/middleware/tool_error/ToolErrorMiddleware) [Class

### TriggerClause

Dictionary-based trigger specification for AND conditions.](/python/langchain/agents/middleware/summarization/TriggerClause) [Class

### SummarizationMiddleware

Summarizes conversation history when token limits are approached.](/python/langchain/agents/middleware/summarization/SummarizationMiddleware) [Class

### ModelFallbackMiddleware

Automatic fallback to alternative models on errors.](/python/langchain/agents/middleware/model_fallback/ModelFallbackMiddleware) [Class

### ModelRetryMiddleware

Middleware that automatically retries failed model calls with configurable backoff.](/python/langchain/agents/middleware/model_retry/ModelRetryMiddleware) [Class

### LLMToolEmulator

Emulates specified tools using an LLM instead of executing them.](/python/langchain/agents/middleware/tool_emulator/LLMToolEmulator) [Class

### InternalCallTransformer

Keep internal model calls out of `run.messages` and the raw event log.](/python/langchain/agents/middleware/internal_call_transformer/InternalCallTransformer)

## Functions

[Function

### create\_agent

Creates an agent graph that calls tools in a loop until a stopping condition is met.](/python/langchain/agents/factory/create_agent) [Function

### shell\_tool](/python/langchain/agents/middleware/shell_tool/ShellToolMiddleware/__init__/shell_tool) [Function

### detect\_email

Detect email addresses in content.](/python/langchain/agents/middleware/_redaction/detect_email) [Function

### detect\_credit\_card

Detect credit card numbers in content using Luhn validation.](/python/langchain/agents/middleware/_redaction/detect_credit_card) [Function

### detect\_ip

Detect IPv4 or IPv6 addresses in content.](/python/langchain/agents/middleware/_redaction/detect_ip) [Function

### detect\_mac\_address

Detect MAC addresses in content.](/python/langchain/agents/middleware/_redaction/detect_mac_address) [Function

### detect\_url

Detect URLs in content using regex and stdlib validation.](/python/langchain/agents/middleware/_redaction/detect_url) [Function

### apply\_strategy

Apply the configured strategy to matches within content.](/python/langchain/agents/middleware/_redaction/apply_strategy) [Function

### resolve\_detector

Return a callable detector for the given configuration.](/python/langchain/agents/middleware/_redaction/resolve_detector) [Function

### write\_todos

Create and manage a structured task list for your current work session.](/python/langchain/agents/middleware/todo/write_todos) [Function

### validate\_retry\_params

Validate retry parameters.](/python/langchain/agents/middleware/_retry/validate_retry_params) [Function

### should\_retry\_exception

Check if an exception should trigger a retry.](/python/langchain/agents/middleware/_retry/should_retry_exception) [Function

### calculate\_delay

Calculate delay for a retry attempt with exponential backoff and optional jitter.](/python/langchain/agents/middleware/_retry/calculate_delay) [Function

### glob\_search

Fast file pattern matching tool that works with any codebase size.](/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware/__init__/glob_search) [Function

### grep\_search

Fast content search tool that works with any codebase size.](/python/langchain/agents/middleware/file_search/FilesystemFileSearchMiddleware/__init__/grep_search) [Function

### hook\_config

Decorator to configure hook behavior in middleware methods.](/python/langchain/agents/middleware/types/hook_config) [Function

### before\_model

Decorator used to dynamically create a middleware with the `before_model` hook.](/python/langchain/agents/middleware/types/before_model) [Function

### after\_model

Decorator used to dynamically create a middleware with the `after_model` hook.](/python/langchain/agents/middleware/types/after_model) [Function

### before\_agent

Decorator used to dynamically create a middleware with the `before_agent` hook.](/python/langchain/agents/middleware/types/before_agent) [Function

### after\_agent

Decorator used to dynamically create a middleware with the `after_agent` hook.](/python/langchain/agents/middleware/types/after_agent) [Function

### dynamic\_prompt

Decorator used to dynamically generate system prompts for the model.](/python/langchain/agents/middleware/types/dynamic_prompt) [Function

### wrap\_model\_call

Create middleware with `wrap_model_call` hook from a function.](/python/langchain/agents/middleware/types/wrap_model_call) [Function

### wrap\_tool\_call

Create middleware with `wrap_tool_call` hook from a function.](/python/langchain/agents/middleware/types/wrap_tool_call) [Function

### configure\_trace\_policy

Set the process-wide default `TracePolicy` for agent middleware hook spans.](/python/langchain/agents/middleware/_trace_policy/configure_trace_policy) [Function

### internal\_call\_metadata

Return metadata that marks a model call as internal to middleware.](/python/langchain/agents/middleware/internal_call_transformer/internal_call_metadata) [Function

### init\_chat\_model

Initialize a chat model from any supported provider using a unified interface.](/python/langchain/chat_models/base/init_chat_model) [Function

### init\_embeddings

Initialize an embedding model from a model name and optional provider.](/python/langchain/embeddings/base/init_embeddings)

## Modules

[Module

### langchain

Main entrypoint into LangChain.](/python/langchain/langchain) [Module

### agents

Entrypoint to building Agents with LangChain.](/python/langchain/agents) [Module

### structured\_output

Types for setting agent response formats.](/python/langchain/agents/structured_output) [Module

### factory

Agent factory for creating agents with middleware support.](/python/langchain/agents/factory) [Module

### middleware

Entrypoint to using middleware plugins with Agents.](/python/langchain/agents/middleware) [Module

### tool\_retry

Tool retry middleware for agents.](/python/langchain/agents/middleware/tool_retry) [Module

### tool\_call\_limit

Tool call limit middleware for agents.](/python/langchain/agents/middleware/tool_call_limit) [Module

### context\_editing

Context editing middleware.](/python/langchain/agents/middleware/context_editing) [Module

### shell\_tool

Middleware that exposes a persistent shell tool to agents.](/python/langchain/agents/middleware/shell_tool) [Module

### tool\_selection

LLM-based tool selector middleware.](/python/langchain/agents/middleware/tool_selection) [Module

### todo

Planning and task management middleware for agents.](/python/langchain/agents/middleware/todo) [Module

### model\_call\_limit

Call tracking middleware for agents.](/python/langchain/agents/middleware/model_call_limit) [Module

### file\_search

File search middleware for Anthropic text editor and memory tools.](/python/langchain/agents/middleware/file_search) [Module

### provider\_tool\_search

Provider-side tool search middleware.](/python/langchain/agents/middleware/provider_tool_search) [Module

### pii

PII detection and handling middleware for agents.](/python/langchain/agents/middleware/pii) [Module

### types

Types for middleware and agents.](/python/langchain/agents/middleware/types) [Module

### human\_in\_the\_loop

Human in the loop middleware.](/python/langchain/agents/middleware/human_in_the_loop) [Module

### tool\_error

Tool error middleware for agents.](/python/langchain/agents/middleware/tool_error) [Module

### summarization

Summarization middleware.](/python/langchain/agents/middleware/summarization) [Module

### model\_fallback

Model fallback middleware for agents.](/python/langchain/agents/middleware/model_fallback) [Module

### model\_retry

Model retry middleware for agents.](/python/langchain/agents/middleware/model_retry) [Module

### tool\_emulator

Tool emulator middleware for testing.](/python/langchain/agents/middleware/tool_emulator) [Module

### internal\_call\_transformer

Tag and filter middleware-internal model calls.](/python/langchain/agents/middleware/internal_call_transformer) [Module

### messages

Message and message content types.](/python/langchain/messages) [Module

### rate\_limiters

Base abstraction and in-memory implementation of rate limiters.](/python/langchain/rate_limiters) [Module

### chat\_models

Entrypoint to using chat models in LangChain.](/python/langchain/chat_models) [Module

### base

Factory functions for chat models.](/python/langchain/chat_models/base) [Module

### tools

Tools.](/python/langchain/tools) [Module

### tool\_node

Utils file included for backwards compat imports.](/python/langchain/tools/tool_node) [Module

### embeddings

Embeddings models.](/python/langchain/embeddings) [Module

### base

Factory functions for embeddings.](/python/langchain/embeddings/base)

## Types

[Type

### ResponseFormat

Union type for all supported response format strategies.](/python/langchain/agents/structured_output/ResponseFormat) [Type

### OnParsingFailure

Behavior when the selection model keeps returning a malformed response.](/python/langchain/agents/middleware/tool_selection/OnParsingFailure) [Type

### RetryOn

Type for specifying which exceptions to retry on.](/python/langchain/agents/middleware/_retry/RetryOn) [Type

### OnFailure

Type for specifying failure handling behavior.](/python/langchain/agents/middleware/_retry/OnFailure) [Type

### ToolIdentifier

Tool name or tool instance that can be deferred behind provider tool search.](/python/langchain/agents/middleware/provider_tool_search/ToolIdentifier) [Type

### ModelCallResult

Return type for model call handlers.](/python/langchain/agents/middleware/types/ModelCallResult) [Type

### Decision](/python/langchain/agents/middleware/human_in_the_loop/Decision) [Type

### ContextSize

Union type for context size specifications.](/python/langchain/agents/middleware/summarization/ContextSize)
