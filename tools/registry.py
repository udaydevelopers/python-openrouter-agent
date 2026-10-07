from tools.calculator import calculate
from tools.datetime_tool import get_current_datetime
from tools.text_analyzer import analyze_text
from tools.weather import get_weather

# ==================================================
# Tool Registry
# ==================================================

TOOL_REGISTRY = {

    "calculate": calculate,

    "get_current_datetime": get_current_datetime,

    "analyze_text": analyze_text,

    "get_weather": get_weather
}


# ==================================================
# OpenRouter Tool Definitions
# ==================================================

TOOL_DEFINITIONS = [

    {
        "type": "function",

        "function": {

            "name": "calculate",

            "description":
                "Perform mathematical calculations such as "
                "addition, subtraction, multiplication and division.",

            "parameters": {

                "type": "object",

                "properties": {

                    "a": {
                        "type": "number",
                        "description": "First number"
                    },

                    "b": {
                        "type": "number",
                        "description": "Second number"
                    },

                    "operation": {

                        "type": "string",

                        "enum": [
                            "add",
                            "subtract",
                            "multiply",
                            "divide"
                        ],

                        "description":
                            "Mathematical operation"
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

            "description":
                "Get the current date, time and day.",

            "parameters": {

                "type": "object",

                "properties": {},

                "required": []
            }
        }
    },


    {
        "type": "function",

        "function": {

            "name": "analyze_text",

            "description":
                "Analyze text and return word count, "
                "character count and line count.",

            "parameters": {

                "type": "object",

                "properties": {

                    "text": {

                        "type": "string",

                        "description":
                            "Text to analyze"
                    }

                },

                "required": [
                    "text"
                ]
            }
        }
    },
    # ==================================================
    # Weather
    # ==================================================

    {
        "type": "function",

        "function": {

            "name":
                "get_weather",

            "description":
                "Get the current weather for a city. "
                "Returns temperature, feels-like temperature, "
                "humidity, precipitation, wind speed and "
                "weather condition.",

            "parameters": {

                "type": "object",

                "properties": {

                    "city": {

                        "type": "string",

                        "description":
                            "City name, for example Bangalore, "
                            "Mumbai, Delhi or London"
                    }
                },

                "required": [

                    "city"
                ]
            }
        }
    }

]


# ==================================================
# Get Tool
# ==================================================

def get_tool(tool_name):

    return TOOL_REGISTRY.get(tool_name)


# ==================================================
# Execute Tool
# ==================================================

def execute_tool(tool_name, arguments):

    tool = get_tool(tool_name)


    if tool is None:

        return {
            "error":
                f"Tool '{tool_name}' is not registered"
        }


    try:

        result = tool(**arguments)

        return result

    except Exception as error:

        return {
            "error": str(error)
        }