# AUTOGENERATED! DO NOT EDIT! File to edit: wrappers.ipynb (unless otherwise specified).

__all__ = ['add_method', 'add_static_method', 'add_class_method']

# Cell
from functools import wraps # This convenience func preserves name and docstring


# Cell
def add_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator


# Cell
def add_static_method(cls):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        return func # returning func means func can still be used normally
    return decorator

# Cell
def add_class_method(cls):
    def decorator(func):
        @wraps(func)
        @classmethod
        def wrapper(cls, *args, **kwargs):
            return func( cls, *args, **kwargs)
        setattr(cls, func.__name__, wrapper)
        # Note we are not binding func, but wrapper which accepts self but does exactly the same as func
        return func # returning func means func can still be used normally
    return decorator