from functools import wraps
from flask import session, abort, redirect, url_for, request


def check_argument(key):
    """Check argument."""

    def __param(func):
        @wraps(func)
        def decorator(*args, **kwargs):
            if key not in kwargs:
                abort(400)
            value = kwargs[key]
            if not value:
                abort(400)
            return func(*args, **kwargs)

        return decorator

    return __param


def query_argument(func):
    """Query argument"""

    @wraps(func)
    def decorator(*args, **kwargs):
        kwargs.update(request.args)
        return func(*args, **kwargs)

    return decorator


def form_argument(func):
    """Form argument."""

    @wraps(func)
    def decorator(*args, **kwargs):
        kwargs.update(request.form.items())
        kwargs.update(request.files.items())
        return func(*args, **kwargs)

    return decorator
