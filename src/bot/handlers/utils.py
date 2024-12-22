import inspect
from typing import Callable, Any

from aiogram.types import Message

from src.domain.users import views as user_views
from src.domain.users.bootstrap import bootstrap as users_bootstrap


users_bootstrap = users_bootstrap()


def auth_decorator(func: Callable) -> Any:
    async def wrapper(*args, **kwargs):
        if message := next(filter(lambda a: isinstance(a, Message), args), None):
            if not (user := await user_views.get_user(message.from_user.id, users_bootstrap.uow)):
                return
            sig_params = extend_parameters(func, user, users_bootstrap)
            await func(*args, **sig_params)
        else:
            await func(*args, **kwargs)
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
