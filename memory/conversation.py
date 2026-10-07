import json
import os


# ==================================================
# Memory Configuration
# ==================================================

MEMORY_DIR = "memory"

MEMORY_FILE = os.path.join(
    MEMORY_DIR,
    "conversation.json"
)


# ==================================================
# Create Memory File
# ==================================================

def initialize_memory():

    if not os.path.exists(MEMORY_DIR):

        os.makedirs(MEMORY_DIR)


    if not os.path.exists(MEMORY_FILE):

        with open(
            MEMORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=2
            )


# ==================================================
# Load Memory
# ==================================================

def load_memory():

    initialize_memory()


    try:

        with open(
            MEMORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)


    except (
        json.JSONDecodeError,
        FileNotFoundError
    ):

        return []


# ==================================================
# Save Memory
# ==================================================

def save_memory(messages):

    initialize_memory()


    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            messages,
            file,
            indent=2,
            ensure_ascii=False
        )


# ==================================================
# Add Message
# ==================================================

def add_message(
    messages,
    message
):

    messages.append(
        message
    )

    save_memory(
        messages
    )


# ==================================================
# Clear Memory
# ==================================================

def clear_memory():

    initialize_memory()


    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            [],
            file,
            indent=2
        )


# ==================================================
# Get Memory
# ==================================================

def get_memory():

    return load_memory()