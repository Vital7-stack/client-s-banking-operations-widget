import functools
from datetime import datetime

def log(filename=None):
    """
    Декоратор для логирования выполнения функций.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__

            # Форматируем входные параметры
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            signature = ", ".join(args_repr + kwargs_repr)

            # Записываем начало выполнения с текущей временной меткой
            timestamp_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_message_start = f"[{timestamp_start}] {func_name} called with: {signature}"

            if filename:
                with open(filename, 'a', encoding='utf-8') as f:
                    f.write(log_message_start + '\n')
            else:
                print(log_message_start)

            try:
                result = func(*args, **kwargs)
                # Обновляем временную метку для сообщения об успехе
                timestamp_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_output = f"[{timestamp_end}] {func_name} ok"

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_output + '\n')
                else:
                    print(log_output)

                return result

            except Exception as e:
                # Обновляем временную метку для сообщения об ошибке
                timestamp_error = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                error_type = type(e).__name__
                log_output = (f"[{timestamp_error}] {func_name} error: {error_type}. "
                             f"Inputs: {args!r}, {kwargs!r}")

                if filename:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_output + '\n')
                else:
                    print(log_output)

                raise

        return wrapper
    return decorator