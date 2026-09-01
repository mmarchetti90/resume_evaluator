#!/usr/bin/env python3

### IMPORTS -------------------------------- ###

from datetime import datetime

### FUNCTIONS ------------------------------ ###

def log_trace(trace_message: str, timestamp: bool=True) -> None:

    """
    Logs a time-stamped trace message to the console

    Parameters
    ----------
    trace_message: str
        The message to log
    timestamp: bool=True
        Set to true to prepend a timestamp
    """

    if timestamp:
        trace_timestamp = datetime.now().strftime("%H:%M:%S")
        timestamped_trace_message = f"[{trace_timestamp}] {trace_message}"
        print(timestamped_trace_message)
    else:
        print(trace_message)
