import time
from functools import wraps


def retry(retry_times=3, fixed_sleep=10, retry_on_exception=Exception):
    """
    重试装饰器
    :param func:
    :param retry_times:
    :param fixed_sleep:
    :param retry_on_exception:
    :return:
    """

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    return func(*args, **kwargs)
                except retry_on_exception as e:
                    if fixed_sleep > 0:
                        time.sleep(fixed_sleep)
            return func(*args, **kwargs)

        return wrapped

    return decorator
