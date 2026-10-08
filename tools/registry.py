from tools.calculator import calculate
from tools.datetime_tool import get_current_datetime
from tools.text_analyzer import analyze_text
from tools.weather import get_weather
from tools.memory_tool import memory_search

from rag.search import search_documents
from rag.vector_store import build_vector_store

from tools.web_search import web_search


TOOL_REGISTRY = {
    "calculate": calculate,
    "get_current_datetime": get_current_datetime,
    "analyze_text": analyze_text,
    "get_weather": get_weather,
    "memory_search": memory_search,
    "search_documents": search_documents,
    "build_vector_store": build_vector_store,
    "web_search": web_search
}


TOOL_DEFINITIONS = [

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform a mathematical calculation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number"
                    },
                    "b": {
                        "type": "number"
                    },
                    "operation": {
                        "type": "string",
                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ]
                    }
                },
                "required": [
                    "a",
                    "b",
                    "operation"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "analyze_text",
            "description": "Analyze text.",
            "parameters": {
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string"
                    }
                },
                "required": [
                    "text"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string"
                    }
                },
                "required": [
                    "city"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "memory_search",
            "description": "Search previous conversations.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "limit": {
                        "type": "integer"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_documents",
            "description": (
                "Search the local knowledge base "
                "using vector similarity."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "top_k": {
                        "type": "integer"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "build_vector_store",
            "description": (
                "Build the local vector database "
                "from documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": (
                "Search the live web for current "
                "or external information."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "limit": {
                        "type": "integer"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    }
]


def get_tool(tool_name):

    return TOOL_REGISTRY.get(
        tool_name
    )


def execute_tool(
    tool_name,
    arguments
):

    tool = get_tool(
        tool_name
    )

    if tool is None:

        return {
            "error": (
                f"Tool '{tool_name}' "
                "is not registered."
            )
        }

    try:

        return tool(
            **arguments
        )

    except Exception as error:

        return {
            "error": str(error)
        }