"""
helper.py
=========
Simple helper functions used in this project
"""


from threading import Thread
from functools import wraps


def run_async(func):
    """
    This decorator help to run a async function
    """

    @wraps(func)
    def async_func(*args, **kwargs):
        my_thread = Thread(target=func, args=args, kwargs=kwargs)
        my_thread.start()
        return my_thread

    return async_func
