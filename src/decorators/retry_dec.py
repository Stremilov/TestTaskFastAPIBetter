import time
import asyncio
from functools import wraps


def retry(times=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt < times:
                        print(f"Retrying {func.__name__} due to {e}, attempt {attempt}/{times}...")
                        time.sleep(delay)
                    else:
                        print(f"Failed after {times} attempts.")
                        raise
        return wrapper
    return decorator


def async_retry(times=3, delay=1, exceptions=(Exception,)):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < times:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    attempt += 1
                    if attempt < times:
                        print(f"Retrying {func.__name__} due to {e}, attempt {attempt}/{times}...")
                        await asyncio.sleep(delay)
                    else:
                        print(f"Failed after {times} attempts.")
                        raise
        return wrapper
    return decorator
