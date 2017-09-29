from functools import wraps

def celery_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def mail_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return True
    return wrapper
