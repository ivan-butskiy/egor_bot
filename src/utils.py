# from threading import Lock, Thread
# from functools import wraps


# class ThreadSafeSingleton(type):
#     _instances = {}
#     _lock: Lock = Lock()
#
#     def __call__(cls, *args, **kwargs):
#         with cls._lock:
#             if cls not in cls._instances:
#                 instance = super().__call__(*args, **kwargs)
#                 cls._instances[cls] = instance
#         return cls._instances[cls]
#
#
# def run_in_thread(func):
#
#     @wraps(func)
#     def inner(*args, **kwargs):
#         Thread(target=func, args=args, kwargs=kwargs).start()
#     return inner
