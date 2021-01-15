"""Универсальный валидатор."""
import re
from typing import Any, Callable

import jsonschema
from jsonschema import validate


def input_validator(in_file: dict) -> Any:
    """Валидатор входных данных."""
    schema = {
        "title": "Validate Schema",
        "type": "object",
        "properties": {
            "id": {
                "type": "integer"
            },
            "country": {
                "type": "string"
            },
            "city": {
                "type": "string"
            },
            "street_name": {
                "type": "string"
            },
            "building_number": {
                "type": "integer"
            },
            "status": {
                "type": "string"
            }

        },
        "required": ["id", "city", "street_name", "building_number", "status"]

    }
    print("Проверка входных данных")
    try:
        validate(in_file, schema)
        return in_file
    except jsonschema.exceptions.ValidationError:
        print("Входные данные не соответствуют формату")
        raise Exception("InputParameterVerificationError")


def result_validator(status: str) -> bool:
    """Валидатор выходных данных."""
    print("Проверка статуса подтверждения адреса")
    res = re.fullmatch(r"(?i)(Проверено|В\sпроцессе|Отклонено)", status)
    if bool(res) is not None:
        print("Выходные данные успешно прошли проверку")
        return bool(res)
    else:
        print("Выходные данные не прошли проверку соотвествия статусу")
        raise Exception("ResultVerificationError")


def default_behaviour() -> None:
    """Дефолтная функция."""
    print("Счётчик отработал. Выход из алгоритма")


class CounterError(Exception):
    """исключение, когда счётчик установлен в 0."""

    def __init__(self) -> None:
        """инициализация счётчика."""
        print("Cчётчик устанвлен в 0. Измените значение")


def decorator(input_validator: Callable, result_validator: Callable,
              on_fail_repeat_times: int = 1, default_behaviour: Callable = None) -> Callable:
    """Декоратор для валидации данных."""
    if on_fail_repeat_times == 0:
        raise CounterError

    def decorator_wrapper(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Callable:
            print("Запуск декоратора")
            if on_fail_repeat_times < 0:
                while True:
                    try:
                        inp = input_validator(*args, **kwargs)
                        out = result_validator(dict(*args, **kwargs)['status'])

                        if inp and out:
                            print("Валидация пройдена")
                        break
                    except Exception:
                        raise Exception("ResultVerificationError")
            else:
                for i in range(1, on_fail_repeat_times + 1):
                    try:
                        input_res = input_validator(*args, **kwargs)
                        out_res = result_validator(dict(*args, **kwargs)['status'])
                        if input_res and out_res:
                            print("Валидация пройдена")
                            break
                    except Exception:
                        raise Exception("ResultVerificationError")
                        if default_behaviour is not None and i == on_fail_repeat_times:
                            default_behaviour()
                            return False
                        if i == on_fail_repeat_times:
                            return False
                        print("Запуск главной фуекции")
                        r = func(*args)
                        return r

        return wrapper

    return decorator_wrapper


@decorator(input_validator, result_validator,
           on_fail_repeat_times=3, default_behaviour=None)
def fnc(file: dict) -> str:
    """функция, которая получает json-файл."""
    s = "Получен адрес для проверки"
    print(s)
    return s
