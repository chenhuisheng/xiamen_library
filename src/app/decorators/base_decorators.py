import hashlib
from functools import wraps
from datetime import datetime
from flask import current_app
from app import cache

def run_times(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        start = datetime.now()
        res = func(*args, **kwargs)
        end = datetime.now()
        delta = end - start
        current_app.logger.info(delta.total_seconds())
        return res
    return decorated_view

def cache_func(timeout):
    def decorator(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            cache_key = '{}{}{}{}'.format(func.__module__, func.__name__, str(args), str(kwargs)).encode('utf-8')
            cache_key = str(hashlib.md5(cache_key).hexdigest())
            res = cache.get(cache_key)
            if res:
                return res
            try:
                res = func(*args, **kwargs)
            except Exception as e:
                return func(*args, **kwargs)
            cache.set(cache_key, res, timeout=timeout)
            return res
        return decorated_view
    return decorator