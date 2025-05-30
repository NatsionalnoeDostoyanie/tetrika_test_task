import inspect
from functools import (
    reduce,
    wraps,
)
from itertools import combinations
from types import UnionType
from typing import (
    Callable,
    ParamSpec,
    TypeVar,
    Unpack,
    get_origin,
    get_type_hints,
    overload,
)


P = ParamSpec("P")
R = TypeVar("R")

# DON'T ADD PARAMETRIZED GENERIC TYPES
ALLOWED_TYPES_BASE = (bool, int, float, str)

allowed_types = tuple(
    reduce(lambda a, b: a | b, types_group)  # type: ignore[arg-type, return-value]
    for r in range(1, len(ALLOWED_TYPES_BASE) + 1)
    for types_group in combinations(ALLOWED_TYPES_BASE, r)
)


@overload
def strict(_func: Callable[P, R]) -> Callable[P, R]: ...


@overload
def strict(
    *, skip_first_argument: bool = False
) -> Callable[[Callable[P, R]], Callable[P, R]]: ...


def strict(
    _func: Callable[P, R] | None = None,
    *,
    skip_first_argument: bool = False,
) -> Callable[P, R] | Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        func_singature = inspect.signature(func)
        func_type_hints = get_type_hints(func)
        type_vars = []
        type_var_tuple_arg = None
        for argument_name, argument_type in func_type_hints.items():
            if argument_name == "return":
                continue
            if get_origin(argument_type) is Unpack:
                type_var_tuple_arg = argument_name
            elif isinstance(argument_type, TypeVar):
                if argument_type.__bound__ not in (*allowed_types, None):
                    raise TypeError(
                        f"Bound of TypeVar argument '{argument_name}' "
                        f"must be one of {allowed_types}, "
                        f"but found '{argument_type.__bound__}' instead"
                    )
                for constraint in argument_type.__constraints__:
                    if constraint not in allowed_types:
                        raise TypeError(
                            f"Constraints of TypeVar argument '{argument_name}' "
                            f"must be in {allowed_types}, "
                            f"but found '{constraint}' instead"
                        )
                type_vars.append(argument_name)
            elif argument_type not in allowed_types:
                raise TypeError(
                    f"The type annotation for argument '{argument_name}' "
                    f"in the function signature must be one of {allowed_types}, "
                    f"but found '{argument_type}' instead"
                )

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            bound_arguments = func_singature.bind(*args, **kwargs)
            bound_arguments.apply_defaults()
            type_vars_to_its_actual_types = {}

            for argument_name, argument_value in (
                tuple(bound_arguments.arguments.items())[1:]
                if skip_first_argument
                else bound_arguments.arguments.items()
            ):
                if argument_name in type_vars:
                    type_var_argument = func_type_hints[argument_name]
                    if type_var_argument not in type_vars_to_its_actual_types:
                        if type_var_argument_bound := type_var_argument.__bound__:
                            type_var_allowed_types: tuple[
                                type[bool]
                                | type[int]
                                | type[float]
                                | type[str]
                                | UnionType,
                                ...,
                            ] = (type_var_argument_bound,)
                        elif (
                            type_var_argument_constraints := type_var_argument.__constraints__
                        ):
                            type_var_allowed_types = type_var_argument_constraints
                        else:
                            type_var_allowed_types = allowed_types
                        if (
                            argument_value_type := type(argument_value)
                        ) not in type_var_allowed_types:
                            raise TypeError(
                                f"Argument '{argument_name}' "
                                f"must be one of {type_var_allowed_types}, "
                                f"but received value of type '{argument_value_type}"
                            )
                        type_vars_to_its_actual_types[type_var_argument] = (
                            argument_name,  # Only for exception logs
                            argument_value_type,
                        )
                    else:
                        if not isinstance(
                            argument_value,
                            type_vars_to_its_actual_types[type_var_argument][1],
                        ):
                            raise TypeError(
                                f"TypeVar arguments types must match: "
                                f"'{argument_name}' has type {type(argument_value)}, "
                                f"which is not equal to '{
                                    type_vars_to_its_actual_types[
                                        type_var_argument
                                    ][0]
                                }', "
                                f"that has type '{
                                    type_vars_to_its_actual_types[
                                        type_var_argument
                                    ][1]
                                }'"
                            )
                elif argument_name == type_var_tuple_arg:
                    for i, arg in enumerate(argument_value):
                        if type(arg) not in allowed_types:
                            raise TypeError(
                                f"Argument '{argument_name}[{i}]' "
                                f"must be one of {allowed_types}, "
                                f"but received value of type '{type(arg)}' "
                            )
                elif not func_type_hints.get(argument_name):
                    if (
                        argument_value_type := type(argument_value)
                    ) not in allowed_types:
                        raise TypeError(
                            f"Argument '{argument_name}' "
                            f"must be one of {allowed_types}, "
                            f"but received value of type '{argument_value_type}"
                        )
                elif not isinstance(argument_value, func_type_hints[argument_name]):
                    raise TypeError(
                        f"Argument '{argument_name}' "
                        f"must be of type '{func_type_hints[argument_name]}' "
                        f"but received value of type '{type(argument_value)}'"
                    )
            return func(*args, **kwargs)

        return wrapper

    return decorator(_func) if _func else decorator


if __name__ == "__main__":

    @strict
    def sum_two(a: int, b: int) -> int:
        return a + b

    print(sum_two(1, 2))
    print(sum_two(1, 2.4))  # type: ignore[arg-type]
