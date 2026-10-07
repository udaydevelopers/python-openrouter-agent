from datetime import datetime


def get_current_datetime():
    """
    Get the current date and time.
    """

    now = datetime.now()

    return {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A")
    }