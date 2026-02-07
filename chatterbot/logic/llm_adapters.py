"""
LLM Logic Adapters for ChatterBot.

This module provides logic adapters that integrate Large Language Models
as participants in the consensus voting mechanism. LLM adapters can use
other logic adapters as tools via MCP (Model Context Protocol).
"""
import json
from typing import Any, Dict, List, Optional, Union

from chatterbot.logic.logic_adapter import LogicAdapter
from chatterbot.conversation import Statement
from chatterbot.logic.mcp_tools import (
    is_tool_adapter,
    convert_to_openai_tool_format,
    convert_to_ollama_tool_format
)
from chatterbot import utils


# Note: The following models are known to support native tool/function calling.
# This list is informational only - actual detection uses template inspection.
# Ollama models with tool support (as of 2026):
# - Llama Series: llama3.1, llama3.2, llama3-groq-tool-use
# - Mistral Series: mistral (v0.3+), mistral-nemo, mistral-large
# - Qwen Series: qwen2.5, qwen2.5-coder
# - Specialized: firefunction-v2, nemotron, nemotron-mini, command-r, command-r-plus
# - Enterprise: granite3.1-dense, hermes3


class LLMLogicAdapter(LogicAdapter):
    """
    Base class for Large Language Model logic adapters.

    .. warning::
        LLM logic adapters are experimental and may change in future releases.
        Tool calling functionality is still being refined and may have limitations.

    LLM adapters participate in ChatterBot's consensus voting mechanism
    alongside traditional logic adapters. They can also use other logic
    adapters as tools through MCP.

    Configuration parameters:
        model (str): The LLM model name (required)
        host (str): API endpoint URL (optional, provider-specific default)
        logic_adapters_as_tools (list): List of logic adapters to expose as tools
        force_native_tools (bool): Force native tool calling (None=auto-detect)
        min_confidence (float): Minimum confidence for LLM responses (default: 0.5)
        max_confidence (float): Maximum confidence for LLM responses (default: 0.85)
        conversation_context_count (int): Number of previous statements to include (default: 5)
        system_message (str): Custom system message for LLM
        input_scanners (list): Input security scanners (None=defaults, []=disabled, list=custom)
        output_scanners (list): Output security scanners (None=defaults, []=disabled, list=custom)
        security_fail_fast (bool): Stop at first security violation (default: False)
        security_raise_on_violation (bool): Raise exception on violation (default: False)
        security_default_response (str): Response when output rejected

    Example:
        {
            'import_path': 'chatterbot.logic.OllamaLogicAdapter',
            'model': 'llama3.1',
            'logic_adapters_as_tools': [
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter'
            ],
            'min_confidence': 0.6,
            'max_confidence': 0.9
        }
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        # Model configuration
        self.model = kwargs.get('model')
        if not self.model:
            raise ValueError("LLM logic adapters require a 'model' parameter")

        self.host = kwargs.get('host')

        # Confidence range for LLM responses (for consensus voting)
        self.min_confidence = kwargs.get('min_confidence', 0.5)
        self.max_confidence = kwargs.get('max_confidence', 0.85)

        # Conversation context
        self.conversation_context_count = kwargs.get('conversation_context_count', 5)

        # System message
        self.system_message = kwargs.get(
            'system_message',
            "You are a helpful AI assistant. Please keep responses concise, conversational, and responses under 1100 tokens."
        )

        # Scanner configuration
        # None = use defaults (enabled), [] = explicitly disabled, List = custom scanners
        self.input_scanners = kwargs.get('input_scanners', None)
        self.output_scanners = kwargs.get('output_scanners', None)

        # Security behavior
        self.security_fail_fast = kwargs.get('security_fail_fast', False)  # Stop at first violation
        self.security_raise_on_violation = kwargs.get('security_raise_on_violation', False)  # Raise exception
        self.security_default_response = kwargs.get(
            'security_default_response',
            "I cannot provide that information."  # Response when output rejected
        )

        # Initialize security scanners if enabled (enabled = scanners not explicitly disabled)
        self._llm_guard_available = False
        if self.input_scanners != [] or self.output_scanners != []:
            self._initialize_security_scanners()

        # Tool calling configuration
        self.force_native_tools = kwargs.get('force_native_tools', None)
        self.tool_registry = {}

        # Initialize tool adapters if provided
        logic_adapters_as_tools = kwargs.get('logic_adapters_as_tools', [])
        if logic_adapters_as_tools:
            self._initialize_tool_adapters(logic_adapters_as_tools, **kwargs)

    def _initialize_security_scanners(self):
        """
        Lazy import and validate llm-guard scanners.

        Checks if llm-guard is available and disables security if not installed.
        Logs a warning to guide users to install the optional dependency.
        """
        try:
            import llm_guard
            self._llm_guard_available = True
            self.chatbot.logger.info("Security scanning enabled with llm-guard")
        except ImportError:
            self.chatbot.logger.warning(
                "llm-guard not installed. Security scanning disabled. "
                "Install with: pip install 'chatterbot[security]' or pip install llm-guard"
            )
            self._llm_guard_available = False
            # Disable scanners by setting to empty list
            if self.input_scanners is not None:
                self.input_scanners = []
            if self.output_scanners is not None:
                self.output_scanners = []

    def _scan_input(self, statement: Statement) -> Statement:
        """
        Apply input security scanning.

        Args:
            statement: User input statement to scan

        Returns:
            Scanned statement (sanitized if violations found)
        """
        # Skip if explicitly disabled or llm-guard unavailable
        if self.input_scanners == [] or not self._llm_guard_available:
            return statement

        from chatterbot.preprocessors import llm_guard_input_scanner

        return llm_guard_input_scanner(
            statement,
            scanners=self.input_scanners,
            fail_fast=self.security_fail_fast,
            raise_on_violation=self.security_raise_on_violation
        )

    def _scan_output(self, response: Statement, input_text: str = "") -> Statement:
        """
        Apply output security scanning.

        Args:
            response: Bot response statement to scan
            input_text: Original user input (for context)

        Returns:
            Scanned statement (sanitized or default response if violations found)
        """
        # Skip if explicitly disabled or llm-guard unavailable
        if self.output_scanners == [] or not self._llm_guard_available:
            return response

        from chatterbot.preprocessors import llm_guard_output_scanner

        return llm_guard_output_scanner(
            response,
            input_text=input_text,
            scanners=self.output_scanners,
            fail_fast=self.security_fail_fast,
            default_response=self.security_default_response
        )

    def _initialize_tool_adapters(self, adapter_configs: List[Union[str, Dict]], **kwargs):
        """
        Initialize logic adapters to be used as tools.

        Args:
            adapter_configs: List of adapter import paths or config dicts
            **kwargs: Additional kwargs to pass to adapters
        """
        for adapter_config in adapter_configs:
            # Validate and initialize the adapter
            utils.validate_adapter_class(adapter_config, LogicAdapter)
            adapter = utils.initialize_class(adapter_config, self.chatbot, **kwargs)

            # Check if adapter supports tool functionality
            if is_tool_adapter(adapter):
                tool_name = adapter.get_tool_name()
                self.tool_registry[tool_name] = adapter
                self.chatbot.logger.info(
                    f"Registered tool: {tool_name} from {adapter.__class__.__name__}"
                )
            else:
                self.chatbot.logger.warning(
                    f"Adapter {adapter.__class__.__name__} does not implement MCPToolAdapter, skipping"
                )

    def _get_conversation_context(self, input_statement: Statement) -> List[Dict[str, str]]:
        """
        Retrieve previous conversation context from storage.

        .. warning::
            Context Poisoning Risk: Historical messages are loaded without security scanning.
            If malicious input was stored in previous interactions, it could be injected
            into the LLM context, potentially bypassing current input security measures.

        TODO: Add optional security scanning of conversation context in future release.
              Options to consider:
              - Scan each historical statement before including in context
              - Add `scan_conversation_context` parameter (default False for performance)
              - Cache scanned contexts to avoid repeated scanning
              - Apply lighter-weight scanners (e.g., BanSubstrings only) for performance

        Args:
            input_statement: The current input statement

        Returns:
            List of message dicts in LLM format
        """
        messages = []

        if not input_statement.conversation:
            return messages

        try:
            # Query storage for recent statements in this conversation
            previous_statements = self.chatbot.storage.filter(
                conversation=input_statement.conversation,
                order_by=['id'],
                page_size=self.conversation_context_count * 2  # x2 to account for bot responses
            )

            # Convert to LLM message format
            for stmt in previous_statements:
                # Determine role based on persona
                if stmt.persona and stmt.persona.startswith('bot:'):
                    role = 'assistant'
                else:
                    role = 'user'

                messages.append({
                    'role': role,
                    'content': stmt.text
                })

        except Exception as e:
            self.chatbot.logger.warning(f"Failed to retrieve conversation context: {e}")

        return messages

    def _build_base_messages(self, input_statement: Statement, system_message: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Build base message list for LLM API calls.

        Args:
            input_statement: The input statement
            system_message: Optional system message override

        Returns:
            List of message dicts in LLM format
        """
        messages = [{'role': 'system', 'content': system_message or self.system_message}]
        messages.extend(self._get_conversation_context(input_statement))
        messages.append({'role': 'user', 'content': input_statement.text})
        return messages

    def _format_error_response(self, error: Exception) -> str:
        """
        Format a consistent error response message.

        Args:
            error: The exception that occurred

        Returns:
            Formatted error message string
        """
        return f"I apologize, but I encountered an error: {str(error)}"

    def _supports_native_tools(self) -> bool:
        """
        Determine if the current model supports native tool calling.

        Returns:
            True if native tools are supported
        """
        # If user explicitly set force_native_tools, use that
        if self.force_native_tools is not None:
            return self.force_native_tools

        # Otherwise, auto-detect based on model
        return self._detect_tool_capability()

    def _detect_tool_capability(self) -> bool:
        """
        Detect if the model supports native tool calling.
        Override in subclasses for provider-specific detection.

        Returns:
            True if tools are supported
        """
        return False

    def _get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in the format expected by the LLM provider.
        Override in subclasses for provider-specific formats.

        Returns:
            List of tool definitions
        """
        raise NotImplementedError("Subclasses must implement _get_tools_for_llm()")

    def _execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> str:
        """
        Execute a tool by its name with the given parameters.

        Args:
            tool_name: Name of the tool to execute
            parameters: Tool parameters

        Returns:
            Tool execution result as string
        """
        if tool_name not in self.tool_registry:
            return f"Error: Tool '{tool_name}' not found"

        adapter = self.tool_registry[tool_name]

        try:
            # Validate parameters
            if not adapter.validate_tool_parameters(**parameters):
                return f"Error: Invalid parameters for tool '{tool_name}'"

            # Execute tool
            result = adapter.execute_as_tool(**parameters)

            # Convert result to string if needed
            if not isinstance(result, str):
                result = str(result)

            return result

        except Exception as e:
            self.chatbot.logger.error(f"Tool execution error for '{tool_name}': {e}")
            return f"Error executing tool '{tool_name}': {str(e)}"

    def _handle_native_tool_calling(self, input_statement: Statement) -> Statement:
        """
        Handle tool calling with native LLM support.
        Override in subclasses for provider-specific implementation.

        Args:
            input_statement: The input statement to process

        Returns:
            Response statement with confidence
        """
        raise NotImplementedError("Subclasses must implement _handle_native_tool_calling()")

    def _handle_prompt_based_tool_calling(self, input_statement: Statement) -> Statement:
        """
        Handle tool calling via prompt engineering for models without native support.

        This method guides the LLM to output structured JSON that can be parsed
        and routed to appropriate tools.

        Args:
            input_statement: The input statement to process

        Returns:
            Response statement with confidence
        """
        # Build tool descriptions for prompt
        tool_descriptions = []
        for adapter in self.tool_registry.values():
            schema = adapter.get_tool_schema()
            tool_desc = f"- {schema['name']}: {schema['description']}"
            tool_descriptions.append(tool_desc)

        tools_text = "\n".join(tool_descriptions)

        # Enhanced system message with tool instructions
        system_msg = f"""{self.system_message}

You have access to the following tools:
{tools_text}

To use a tool, respond ONLY with a JSON object in this format:
{{"tool": "tool_name", "parameters": {{"param1": "value1"}}}}

If you don't need to use a tool, respond normally with plain text."""

        # Get LLM response
        response_text = self._call_llm(input_statement, system_msg)

        # Try to parse as JSON (tool call)
        if response_text.strip().startswith('{'):
            try:
                tool_call = json.loads(response_text)
                tool_name = tool_call.get('tool')
                parameters = tool_call.get('parameters', {})

                # Execute tool
                tool_result = self._execute_tool(tool_name, parameters)

                # Get final response from LLM with tool result
                followup_msg = f"Tool '{tool_name}' returned: {tool_result}\nProvide a natural language response to the user."
                final_response = self._call_llm_with_context(input_statement, followup_msg)

                response = Statement(text=final_response)
                response.confidence = self._calculate_confidence(final_response)
                return response

            except json.JSONDecodeError:
                pass  # Not a tool call, treat as normal response

        # Regular text response
        response = Statement(text=response_text)
        response.confidence = self._calculate_confidence(response_text)
        return response

    def _call_llm(self, input_statement: Statement, system_message: Optional[str] = None) -> str:
        """
        Make a direct LLM API call without tool support.
        Override in subclasses for provider-specific implementation.

        Args:
            input_statement: The input statement
            system_message: Optional system message override

        Returns:
            LLM response text
        """
        raise NotImplementedError("Subclasses must implement _call_llm()")

    def _call_llm_with_context(self, input_statement: Statement, additional_context: str) -> str:
        """
        Make an LLM call with additional context message.

        Args:
            input_statement: The input statement
            additional_context: Additional context to include

        Returns:
            LLM response text
        """
        # This will be implemented in subclasses using their specific API
        raise NotImplementedError("Subclasses must implement _call_llm_with_context()")

    def _calculate_confidence(self, response_text: str) -> float:
        """
        Calculate confidence score for LLM response.

        Uses a simple heuristic based on response length and quality indicators.
        Returns a value between min_confidence and max_confidence.

        Args:
            response_text: The LLM's response text

        Returns:
            Confidence score between 0 and 1
        """
        # Base confidence (middle of range)
        confidence = (self.min_confidence + self.max_confidence) / 2

        # Adjust based on response length (very short or very long may be less reliable)
        length = len(response_text)
        if length < 10:
            confidence -= 0.1
        elif 50 < length < 200:
            confidence += 0.05

        # Clamp to configured range
        confidence = max(self.min_confidence, min(self.max_confidence, confidence))

        return confidence

    def process(self, statement: Statement, additional_response_selection_parameters: dict = None) -> Statement:
        """
        Process the input statement using the LLM with security scanning.

        Security scanning is applied in two stages:
        1. Input scanning: Before LLM processing (prevents prompt injection)
        2. Output scanning: After LLM processing (prevents harmful outputs)

        Args:
            statement: The input statement to process
            additional_response_selection_parameters: Additional parameters (unused)

        Returns:
            Response statement with confidence score
        """
        # Stage 1: Scan input for security threats
        scanned_input = self._scan_input(statement)

        # Process with LLM
        # If no tools are configured, just call LLM directly
        if not self.tool_registry:
            response_text = self._call_llm(scanned_input)
            response = Statement(text=response_text)
            response.confidence = self._calculate_confidence(response_text)
        else:
            # Determine tool calling method
            if self._supports_native_tools():
                response = self._handle_native_tool_calling(scanned_input)
            else:
                response = self._handle_prompt_based_tool_calling(scanned_input)

        # Stage 2: Scan output for security/safety issues
        scanned_output = self._scan_output(response, input_text=statement.text)

        return scanned_output


class OllamaLogicAdapter(LLMLogicAdapter):
    """
    Logic adapter for Ollama LLMs with MCP tool support.

    .. warning::
        This adapter is experimental. Tool capability detection uses template
        inspection which may not work for all model formats. Tool calling behavior
        varies significantly between models.

    Configuration:
        model (str): Ollama model name (e.g., 'llama3.1', 'mistral')
        host (str): Ollama API endpoint (default: http://localhost:11434)
        logic_adapters_as_tools (list): Logic adapters to expose as tools

    Example:
        {
            'import_path': 'chatterbot.logic.OllamaLogicAdapter',
            'model': 'llama3.1',
            'host': 'http://localhost:11434',
            'logic_adapters_as_tools': [
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter'
            ]
        }
    """

    def __init__(self, chatbot, **kwargs):
        # Set default host before parent init
        if 'host' not in kwargs:
            kwargs['host'] = 'http://localhost:11434'

        super().__init__(chatbot, **kwargs)

        # Initialize Ollama client
        try:
            from ollama import Client
            self.client = Client(host=self.host)
        except ImportError:
            raise ImportError(
                "Ollama library not installed. Install with: pip install chatterbot[dev]"
            )

    def _detect_tool_capability(self) -> bool:
        """
        Detect if the Ollama model supports native tool calling.

        Uses template inspection to check if the model's template includes
        tool-specific tokens like {{ .Tools }} or {{ tools }}.

        Returns:
            True if model supports tools
        """
        try:
            # Get model metadata
            model_info = self.client.show(self.model)

            # Get the template string
            template = model_info.get('template', '')

            # Check for tool-specific tokens in the template
            has_tools = '{{ .Tools }}' in template or '{{ tools }}' in template

            if has_tools:
                self.chatbot.logger.info(
                    f"Model '{self.model}' supports native tool calling (template inspection)"
                )
            else:
                self.chatbot.logger.info(
                    f"Model '{self.model}' does not support native tool calling, will use prompt-based approach"
                )

            return has_tools

        except Exception as e:
            self.chatbot.logger.warning(
                f"Failed to inspect model '{self.model}' for tool support: {e}. "
                f"Falling back to prompt-based tool calling."
            )
            return False

    def _get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in Ollama format.

        Returns:
            List of Ollama-formatted tool definitions
        """
        tools = []
        for adapter in self.tool_registry.values():
            schema = adapter.get_tool_schema()
            ollama_tool = convert_to_ollama_tool_format(schema)
            tools.append(ollama_tool)
        return tools

    def _call_llm(self, input_statement: Statement, system_message: Optional[str] = None) -> str:
        """
        Call Ollama API without tool support.

        Args:
            input_statement: The input statement
            system_message: Optional system message override

        Returns:
            LLM response text
        """
        # Build messages with conversation context
        messages = self._build_base_messages(input_statement, system_message)

        try:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            self.chatbot.logger.error(f"Ollama API error: {e}")
            return self._format_error_response(e)

    def _call_llm_with_context(self, input_statement: Statement, additional_context: str) -> str:
        """
        Call Ollama with additional context for tool result processing.

        Args:
            input_statement: The input statement
            additional_context: Additional context message

        Returns:
            LLM response text
        """
        messages = self._build_base_messages(input_statement)
        messages.append({'role': 'assistant', 'content': additional_context})

        try:
            response = self.client.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            self.chatbot.logger.error(f"Ollama API error: {e}")
            return self._format_error_response(e)

    def _handle_native_tool_calling(self, input_statement: Statement) -> Statement:
        """
        Handle tool calling with Ollama's native function calling support.

        Args:
            input_statement: The input statement to process

        Returns:
            Response statement with confidence
        """
        # Build messages
        messages = self._build_base_messages(input_statement)

        # Get tools in Ollama format
        tools = self._get_tools_for_llm()

        try:
            # Initial LLM call with tools
            response = self.client.chat(
                model=self.model,
                messages=messages,
                tools=tools
            )

            message = response['message']

            # Check if LLM wants to use a tool
            if tool_calls := message.get('tool_calls'):
                # Execute each tool call
                for tool_call in tool_calls:
                    function = tool_call['function']
                    tool_name = function['name']
                    parameters = function.get('arguments', {})

                    # Execute tool
                    tool_result = self._execute_tool(tool_name, parameters)

                    # Add tool result to conversation
                    messages.append(message)
                    messages.append({
                        'role': 'tool',
                        'content': tool_result
                    })

                # Get final response from LLM with tool results
                final_response = self.client.chat(
                    model=self.model,
                    messages=messages
                )

                response_text = final_response['message']['content']
            else:
                # No tool call, use direct response
                response_text = message['content']

            response = Statement(text=response_text)
            response.confidence = self._calculate_confidence(response_text)
            return response

        except Exception as e:
            self.chatbot.logger.error(f"Ollama tool calling error: {e}")
            response = Statement(text=self._format_error_response(e))
            response.confidence = self.min_confidence
            return response


class OpenAILogicAdapter(LLMLogicAdapter):
    """
    Logic adapter for OpenAI LLMs with MCP tool support.

    .. warning::
        This adapter is experimental. Tool capability is validated via API dry run
        which incurs minimal token costs. Not all OpenAI models support tool calling
        (e.g., o1-preview, legacy completion models).

    OpenAI models have universal tool calling support, so force_native_tools
    is always True unless explicitly disabled.

    Configuration:
        model (str): OpenAI model name (e.g., 'gpt-4', 'gpt-3.5-turbo')
        host (str): Optional custom API endpoint
        logic_adapters_as_tools (list): Logic adapters to expose as tools

    Environment:
        OPENAI_API_KEY: Required for authentication

    Example:
        {
            'import_path': 'chatterbot.logic.OpenAILogicAdapter',
            'model': 'gpt-4o-mini',
            'logic_adapters_as_tools': [
                'chatterbot.logic.MathematicalEvaluation',
                'chatterbot.logic.TimeLogicAdapter'
            ]
        }
    """

    def __init__(self, chatbot, **kwargs):
        super().__init__(chatbot, **kwargs)

        # Initialize OpenAI client
        try:
            from openai import OpenAI as OpenAIClient
            if self.host:
                self.client = OpenAIClient(base_url=self.host)
            else:
                self.client = OpenAIClient()
        except ImportError:
            raise ImportError(
                "OpenAI library not installed. Install with: pip install chatterbot[dev]"
            )

    def _detect_tool_capability(self) -> bool:
        """
        Detect if the OpenAI model supports tool calling.

        Performs a 'dry run' with a minimal request including a dummy tool
        to check if the model accepts the tools parameter.

        Returns:
            True if model supports tools
        """
        try:
            from openai import BadRequestError

            # Perform dry run with dummy tool
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hi"}],
                tools=[{
                    "type": "function",
                    "function": {
                        "name": "dummy_tool",
                        "description": "A test tool",
                        "parameters": {"type": "object", "properties": {}}
                    }
                }],
                max_tokens=1  # Minimize cost/latency
            )

            self.chatbot.logger.info(
                f"Model '{self.model}' supports native tool calling (dry run validation)"
            )
            return True

        except BadRequestError as e:
            # Check specifically for tools-related errors
            if "tools" in str(e).lower() or "not supported" in str(e).lower():
                self.chatbot.logger.info(
                    f"Model '{self.model}' does not support tool calling (API validation), "
                    f"will use prompt-based approach"
                )
            else:
                self.chatbot.logger.warning(
                    f"Unexpected error checking tool support for '{self.model}': {e}"
                )
            return False

        except Exception as e:
            self.chatbot.logger.warning(
                f"Failed to validate tool support for '{self.model}': {e}. "
                f"Falling back to prompt-based tool calling."
            )
            return False

    def _get_tools_for_llm(self) -> List[Dict[str, Any]]:
        """
        Get tool definitions in OpenAI format.

        Returns:
            List of OpenAI-formatted tool definitions
        """
        tools = []
        for adapter in self.tool_registry.values():
            schema = adapter.get_tool_schema()
            openai_tool = convert_to_openai_tool_format(schema)
            tools.append(openai_tool)
        return tools

    def _call_llm(self, input_statement: Statement, system_message: Optional[str] = None) -> str:
        """
        Call OpenAI API without tool support.

        Args:
            input_statement: The input statement
            system_message: Optional system message override

        Returns:
            LLM response text
        """
        # Build messages with conversation context
        messages = self._build_base_messages(input_statement, system_message)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            self.chatbot.logger.error(f"OpenAI API error: {e}")
            return self._format_error_response(e)

    def _call_llm_with_context(self, input_statement: Statement, additional_context: str) -> str:
        """
        Call OpenAI with additional context for tool result processing.

        Args:
            input_statement: The input statement
            additional_context: Additional context message

        Returns:
            LLM response text
        """
        messages = self._build_base_messages(input_statement)
        messages.append({'role': 'assistant', 'content': additional_context})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            self.chatbot.logger.error(f"OpenAI API error: {e}")
            return self._format_error_response(e)

    def _handle_native_tool_calling(self, input_statement: Statement) -> Statement:
        """
        Handle tool calling with OpenAI's native function calling support.

        Args:
            input_statement: The input statement to process

        Returns:
            Response statement with confidence
        """
        # Build messages
        messages = self._build_base_messages(input_statement)

        # Get tools in OpenAI format
        tools = self._get_tools_for_llm()

        try:
            # Initial LLM call with tools
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=tools
            )

            message = response.choices[0].message

            # Check if LLM wants to use a tool
            if tool_calls := message.tool_calls:
                # Execute each tool call
                for tool_call in tool_calls:
                    function = tool_call.function
                    tool_name = function.name
                    parameters = json.loads(function.arguments)

                    # Execute tool
                    tool_result = self._execute_tool(tool_name, parameters)

                    # Add assistant message with tool call
                    messages.append({
                        'role': 'assistant',
                        'content': None,
                        'tool_calls': [{
                            'id': tool_call.id,
                            'type': 'function',
                            'function': {
                                'name': tool_name,
                                'arguments': function.arguments
                            }
                        }]
                    })

                    # Add tool result message
                    messages.append({
                        'role': 'tool',
                        'tool_call_id': tool_call.id,
                        'content': tool_result
                    })

                # Get final response from LLM with tool results
                final_response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )

                response_text = final_response.choices[0].message.content
            else:
                # No tool call, use direct response
                response_text = message.content

            response = Statement(text=response_text)
            response.confidence = self._calculate_confidence(response_text)
            return response

        except Exception as e:
            self.chatbot.logger.error(f"OpenAI tool calling error: {e}")
            response = Statement(text=self._format_error_response(e))
            response.confidence = self.min_confidence
            return response
