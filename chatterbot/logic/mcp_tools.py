"""
MCP (Model Context Protocol) tool adapter for ChatterBot logic adapters.

This module provides a mixin class that allows logic adapters to be exposed
as MCP-compatible tools to LLMs. Logic adapters that inherit from MCPToolAdapter
can define tool schemas and be invoked by LLM adapters.
"""
from typing import Any, Dict
from abc import ABC, abstractmethod


class MCPToolAdapter(ABC):
    """
    Mixin class for logic adapters that can be used as MCP tools.

    Logic adapters that want to be callable as tools should inherit from this
    class and implement the get_tool_schema() and execute_as_tool() methods.

    Example:
        class MathematicalEvaluation(LogicAdapter, MCPToolAdapter):
            def get_tool_schema(self) -> Dict[str, Any]:
                return {
                    "name": "calculate",
                    "description": "Evaluate mathematical expressions",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "expression": {
                                "type": "string",
                                "description": "Mathematical expression to evaluate"
                            }
                        },
                        "required": ["expression"]
                    }
                }

            def execute_as_tool(self, **kwargs) -> str:
                expression = kwargs.get("expression")
                # ... evaluation logic
                return result
    """

    @abstractmethod
    def get_tool_schema(self) -> Dict[str, Any]:
        """
        Return the tool schema for this logic adapter.

        The schema should follow the OpenAI/MCP function calling format:
        {
            "name": "tool_name",
            "description": "Tool description",
            "parameters": {
                "type": "object",
                "properties": {
                    "param_name": {
                        "type": "string|number|boolean|array|object",
                        "description": "Parameter description"
                    }
                },
                "required": ["param_name"]
            }
        }

        Returns:
            Dict containing the tool schema
        """
        raise NotImplementedError(
            "Logic adapters using MCPToolAdapter must implement get_tool_schema()"
        )

    @abstractmethod
    def execute_as_tool(self, **kwargs) -> Any:
        """
        Execute this logic adapter as a tool with the given parameters.

        This method is called when an LLM requests to use this adapter as a tool.
        It should extract the necessary parameters from kwargs and execute the
        logic adapter's functionality in a tool-calling context.

        Args:
            **kwargs: Tool parameters as defined in the tool schema

        Returns:
            Tool execution result (will be converted to string if needed)
        """
        raise NotImplementedError(
            "Logic adapters using MCPToolAdapter must implement execute_as_tool()"
        )

    def get_tool_name(self) -> str:
        """
        Get the name of this tool.

        Returns:
            The tool name from the schema
        """
        schema = self.get_tool_schema()
        return schema.get("name", self.__class__.__name__)

    def validate_tool_parameters(self, **kwargs) -> bool:
        """
        Validate that the provided parameters match the tool schema.

        Args:
            **kwargs: Parameters to validate

        Returns:
            True if parameters are valid, False otherwise
        """
        schema = self.get_tool_schema()
        parameters = schema.get("parameters", {})
        required = parameters.get("required", [])
        properties = parameters.get("properties", {})

        # Check required parameters
        for param in required:
            if param not in kwargs:
                return False

        # Check parameter types (basic validation)
        for param_name, param_value in kwargs.items():
            if param_name not in properties:
                continue

            expected_type = properties[param_name].get("type")
            if expected_type == "string" and not isinstance(param_value, str):
                return False
            elif expected_type == "number" and not isinstance(param_value, (int, float)):
                return False
            elif expected_type == "boolean" and not isinstance(param_value, bool):
                return False
            elif expected_type == "array" and not isinstance(param_value, list):
                return False
            elif expected_type == "object" and not isinstance(param_value, dict):
                return False

        return True


def is_tool_adapter(adapter) -> bool:
    """
    Check if a logic adapter instance supports MCP tool functionality.

    Args:
        adapter: Logic adapter instance to check

    Returns:
        True if the adapter has MCPToolAdapter capabilities
    """
    return (
        hasattr(adapter, 'get_tool_schema') and
        callable(adapter.get_tool_schema) and
        hasattr(adapter, 'execute_as_tool') and
        callable(adapter.execute_as_tool)
    )


def convert_to_openai_tool_format(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MCP tool schema to OpenAI function calling format.

    OpenAI expects:
    {
        "type": "function",
        "function": {
            "name": "...",
            "description": "...",
            "parameters": {...}
        }
    }

    Args:
        schema: MCP tool schema

    Returns:
        OpenAI-formatted tool definition
    """
    return {
        "type": "function",
        "function": {
            "name": schema.get("name"),
            "description": schema.get("description", ""),
            "parameters": schema.get("parameters", {})
        }
    }


def convert_to_ollama_tool_format(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert MCP tool schema to Ollama function calling format.

    Ollama uses a similar format to OpenAI:
    {
        "type": "function",
        "function": {
            "name": "...",
            "description": "...",
            "parameters": {...}
        }
    }

    Args:
        schema: MCP tool schema

    Returns:
        Ollama-formatted tool definition
    """
    # Ollama format is identical to OpenAI for now
    return convert_to_openai_tool_format(schema)
