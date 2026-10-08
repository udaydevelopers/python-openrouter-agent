from tools.calculator import calculate
from tools.datetime_tool import get_current_datetime
from tools.text_analyzer import analyze_text
from tools.weather import get_weather

from rag.search import search_documents
from rag.vector_store import build_vector_store


TOOL_REGISTRY = {
    "calculate": calculate,
    "get_current_datetime": get_current_datetime,
    "analyze_text": analyze_text,
    "get_weather": get_weather,
    "search_documents": search_documents,
    "build_vector_store": build_vector_store
}


TOOL_DEFINITIONS = [

    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": (
                "Perform a mathematical calculation."
            ),
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
            "description": (
                "Get the current date and time."
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
            "name": "analyze_text",
            "description": (
                "Analyze text including "
                "words, characters and lines."
            ),
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
            "description": (
                "Get current weather for a city."
            ),
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
            "name": "search_documents",
            "description": (
                "Search the local knowledge base "
                "for information relevant to a question."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5
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
                "Build or rebuild the local vector "
                "database from documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]


def get_tool(tool_name):

    return TOOL_REGISTRY.get(tool_name)


def execute_tool(
    tool_name,
    arguments
):

    tool = get_tool(tool_name)

    if tool is None:

        return {
            "error": (
                f"Tool '{tool_name}' "
                "is not registered"
            )
        }

    try:

        return tool(**arguments)

    except Exception as error:

        return {
            "error": str(error)
        }