import datetime


def trace_decorator(path):
    def _trace_decorator(some_function):
        def new_function(*args, **kwargs):
            with open(f"{path}\log.txt", "a", encoding="utf-8") as file:
                file.write(
                    f'{datetime.datetime.now()} вызывана функция {some_function.__name__} c аргументами {args} и '
                    f'{kwargs}. ')
                result = some_function(*args, **kwargs)
                file.write(f'Вернули результат {result}\n')
            return result

        return new_function

    return _trace_decorator
