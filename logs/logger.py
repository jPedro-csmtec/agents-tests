import logging
import os
import inspect
from functools import wraps
import time

LOG_DIR = "./"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "application.log")

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_function_call(func):
    """Decorator para logar chamadas de funções, retornos e tempo de execução."""
    is_coroutine = inspect.iscoroutinefunction(func)

    if is_coroutine:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start = time.perf_counter()
            logging.info(f"Chamando função: {func.__name__} com args: {args} kwargs: {kwargs}")
            try:
                result = await func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000  # em ms
                logging.info(f"{func.__name__} retornou: {result} (tempo: {elapsed:.2f} ms)")
                return result
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                logging.error(f"Erro na função {func.__name__} após {elapsed:.2f} ms: {e}")
                raise
    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            logging.info(f"Chamando função: {func.__name__} com args: {args} kwargs: {kwargs}")
            try:
                result = func(*args, **kwargs)
                elapsed = (time.perf_counter() - start) * 1000  # em ms
                logging.info(f"{func.__name__} retornou: {result} (tempo: {elapsed:.2f} ms)")
                return result
            except Exception as e:
                elapsed = (time.perf_counter() - start) * 1000
                logging.error(f"Erro na função {func.__name__} após {elapsed:.2f} ms: {e}")
                raise

    wrapper.__signature__ = inspect.signature(func)
    return wrapper
