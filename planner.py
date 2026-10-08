def create_plan(user_input):
    """
    Create a simple plan from the user's request.
    """

    text = user_input.lower()

    steps = []

    # Math
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

    if any(word in text for word in math_words):
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

    # Date/time
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
            "file",
            "project",
            "knowledge base"
        ]
    ):
        steps.append("rag")

    # No special tool
    if not steps:
        steps.append("llm")

    return steps