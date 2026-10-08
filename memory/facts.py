import json
import os


FACT_FILE = "memory/facts.json"


def initialize_facts():
    """
    Create the memory directory and facts file
    if they do not exist.
    """

    if not os.path.exists("memory"):
        os.makedirs("memory")

    if not os.path.exists(FACT_FILE):

        with open(
            FACT_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=2
            )


def load_facts():
    """
    Load facts safely.

    If the file is empty or contains invalid JSON,
    automatically reset it to an empty list.
    """

    initialize_facts()

    try:

        with open(
            FACT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read().strip()

            if not content:
                return []

            data = json.loads(content)

            if isinstance(data, list):
                return data

            return []

    except (
        json.JSONDecodeError,
        OSError
    ):

        # Recover from corrupted/empty JSON
        save_facts([])

        return []


def save_facts(facts):
    """
    Save facts to JSON.
    """

    initialize_facts()

    with open(
        FACT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            facts,
            file,
            indent=2,
            ensure_ascii=False
        )


def add_fact(fact):
    """
    Add a new fact if it does not already exist.
    """

    if not fact:
        return

    facts = load_facts()

    if fact not in facts:

        facts.append(fact)

        save_facts(facts)


def get_facts():
    """
    Return all stored facts.
    """

    return load_facts()


def clear_facts():
    """
    Remove all stored facts.
    """

    save_facts([])