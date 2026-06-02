import threading

_call_stack = threading.local()

class RecursiveCallPreventer:
    def __init__(self, real_func):
        self._real_func = real_func
        self._func_key = (real_func.__module__, real_func.__name__)

    def __call__(self, *args, **kwargs):
        if not hasattr(_call_stack, "stack"):
            _call_stack.stack = []

        if self._func_key in _call_stack.stack:
            return None

        _call_stack.stack.append(self._func_key)
        try:
            result = self._real_func(*args, **kwargs)
        finally:
            _call_stack.stack.pop()
        return result

    def __hash__(self):
        return hash(self._func_key)

    def __eq__(self, other):
        if isinstance(other, RecursiveCallPreventer):
            return self._func_key == other._func_key
        if hasattr(other, '__module__') and hasattr(other, '__name__'):
            return (self._real_func.__module__, self._real_func.__name__) == (other.__module__, other.__name__)
        return False

    def __repr__(self):
        return f"<RecursiveCallPreventer for {self._real_func}>"