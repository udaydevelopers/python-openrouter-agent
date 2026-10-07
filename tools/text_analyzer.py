def analyze_text(text: str):
    """
    Analyze basic information about a text.
    """

    words = text.split()

    characters = len(text)

    characters_without_spaces = len(
        text.replace(" ", "")
    )

    word_count = len(words)

    lines = text.splitlines()

    line_count = len(lines)

    return {
        "word_count": word_count,
        "character_count": characters,
        "character_count_without_spaces": characters_without_spaces,
        "line_count": line_count
    }