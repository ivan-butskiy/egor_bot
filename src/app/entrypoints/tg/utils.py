import inspect
from typing import Callable, Any
from functools import wraps

from aiogram import types

from src.users import views as user_views
from src.users.bootstrap import bootstrap as users_bootstrap


def auth_decorator(func: Callable) -> Any:
    @wraps(func)
    async def wrapper(*args, **kwargs):
        if event := next(filter(lambda a: isinstance(a, (types.Message, types.CallbackQuery)), args), None):
            if not (user := await user_views.get_user(users_bootstrap.uow, event.from_user.id)):
                return
            sig_params = extend_parameters(func, user, users_bootstrap, *args)
            await func(**sig_params, **kwargs)
        else:
            await func(*args)
    return wrapper


def extend_parameters(func: Callable, *objects, **kwargs) -> dict:
    signature = inspect.signature(func)
    result = {}
    for name, parameter in signature.parameters.items():
        if name in kwargs:
            result[name] = kwargs[name]
        elif obj := next(filter(lambda o: type(o) == parameter.annotation, objects), None):
            result[name] = obj
    return result
