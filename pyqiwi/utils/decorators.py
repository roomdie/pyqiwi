from pydantic import BaseModel
from functools import wraps
from typing import get_type_hints, get_origin, get_args, Annotated
from pyqiwi import types


class MinValue:
    def __init__(self, value):
        self.value = value


def check_annotations(func):
    @wraps(func)
    def wrapped(*args, **kwargs) -> func:
        type_hints = get_type_hints(func, include_extras=True)
        for param, hint in type_hints.items():
            if get_origin(hint) is not Annotated:
                continue
            hint_type, *hint_args = get_args(hint)
            if hint_type is int or get_origin(hint_type) is int:
                for arg in hint_args:
                    if isinstance(arg, MinValue):
                        min_value = arg.value
                        actual_value = kwargs[param]
                        if min_value > actual_value:
                            raise ValueError(f"Parameter '{param}' has minimum value"
                                             f" {min_value} (got value {actual_value}).")
        return func(*args, **kwargs)
    return wrapped


def serializing_json(func):
    @wraps(func)
    def wrapped(*args, **kwargs) -> func:
        for _key, _value in kwargs.items():
            subclass_name: str = _value.__class__.__name__
            subclass_mark = "Cls"
            if not subclass_name.endswith(subclass_mark):
                continue

            subclass = getattr(types, subclass_name[:-len(subclass_mark)])
            if issubclass(subclass, BaseModel):
                x = subclass.from_orm(_value)
                kwargs[_key] = x.dict()
        return func(*args, **kwargs)
    return wrapped


