from time import sleep


def retry(
        attempts: int = 3, delay: float = 10, exceptions: list[type[BaseException]] = None,
):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if exceptions is None:
                return func(*args, **kwargs)
            for _ in range(attempts):
                print(_)
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(exceptions)
                    print(type(e) not in exceptions, exceptions)
                    if type(e) not in exceptions:
                        raise e
                    sleep(delay)
            return None

        return wrapper

    return decorator
