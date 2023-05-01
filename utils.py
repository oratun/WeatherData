import logging
import time
import traceback
from functools import wraps
logger = logging.getLogger(__name__)


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
                    logger.info(f'{func} retrying {retry_times} times')
                    if fixed_sleep > 0:
                        time.sleep(fixed_sleep)
            try:
                func(*args, **kwargs)
            except retry_on_exception:
                logger.error(f'{func} retry failed')
                raise RuntimeError(traceback.format_exc())

        return wrapped

    return decorator
