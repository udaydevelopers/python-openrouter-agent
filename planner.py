def create_plan(user_input):
    """
    Create a simple plan from the user's request.
    """

    text = user_input.lower()

    steps = []

    # Calculator
    math_words = [
        "calculate",
        "plus",
        "minus",
        "multiply",
        "divide",
        "percentage",
        "*",
        "/"
    ]

    if any(
        word in text
        for word in math_words
    ):
        steps.append("calculator")

    # Weather
    if any(
        word in text
        for word in [
            "weather",
            "temperature",
            "rain"
        ]
    ):
        steps.append("weather")

    # Date and time
    if any(
        word in text
        for word in [
            "today",
            "date",
            "time",
            "current time"
        ]
    ):
        steps.append("datetime")

    # Memory
    if any(
        word in text
        for word in [
            "remember",
            "earlier",
            "previous",
            "my name",
            "my information"
        ]
    ):
        steps.append("memory")

    # RAG
    if any(
        word in text
        for word in [
            "document",
            "documents",
            "file",
            "files",
            "knowledge base",
            "according to the document"
        ]
    ):
        steps.append("rag")

    # Web
    web_words = [
        "latest",
        "current",
        "news",
        "today",
        "recent",
        "search",
        "online",
        "internet",
        "website",
        "web"
    ]

    if any(
        word in text
        for word in web_words
    ):
        steps.append("web")

    if not steps:
        steps.append("llm")

    return steps