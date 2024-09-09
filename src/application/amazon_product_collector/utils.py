from time import sleep


def retry(attempts: int = 3, delay: float = 10, exceptions: list[type[BaseException]] = None):
    if exceptions is None:
        exceptions = []

    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if type(e) not in exceptions:
                        raise e
                    sleep(delay)
            return None

        return wrapper

    return decorator
