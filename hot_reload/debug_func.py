import debugpy
import inspect


def debug_func(fn):
    def wrapper(*args, **kwargs):
        debugpy.debug_this_thread()
        return fn(*args, **kwargs)

    wrapper.__name__ = fn.__name__
    wrapper.__signature__ = inspect.signature(fn)

    return wrapper
