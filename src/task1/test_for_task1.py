from itertools import combinations
from typing import (
    MutableSequence,
    Sequence,
    TypeVar,
    TypeVarTuple,
)

import pytest

from task1.solution import (
    ALLOWED_TYPES_BASE,
    allowed_types,
    strict,
)


INVALID_EXAMPLES = {
    MutableSequence: [True, 1, 1.25, "2"],
    Sequence: (True, 1, 1.25, "2"),
    list: [True, 1, 1.25, "2"],
    tuple: (True, 1, 1.25, "2"),
    list[int]: [1, 2, 3, 4],
    tuple[int, str]: (1, "2", 3, "4"),
    tuple[str, ...]: ("1", "2", "3", "4"),
    int | list: [1, 2, 3, 4],
    tuple | list: (1, 2, 3, 4),
}

INVALID_TYPES = INVALID_EXAMPLES.keys()

ALLOWED_EXAMPLES = {
    bool: (True, False),
    int: (-1, 0, 1),
    float: (-1.25, 1.25),
    str: ("", " ", "spam", "\\", "%%"),
}

type_var_constraints_combinations = tuple(
    combo
    for r in range(2, len(ALLOWED_TYPES_BASE) + 1)
    for combo in combinations(ALLOWED_TYPES_BASE, r)
)

type_var_constraints_combinations_invalid = tuple(
    combo
    for r in range(2, len(INVALID_TYPES) + 1)
    for combo in combinations(INVALID_TYPES, r)
)

all_allowed_values_examples = tuple(
    allowed_value
    for allowed_values_tuple in ALLOWED_EXAMPLES.values()
    for allowed_value in allowed_values_tuple
)

all_allowed_values_examples_combinations = tuple(
    combo
    for r in range(1, len(all_allowed_values_examples) + 1)
    for combo in combinations(all_allowed_values_examples, r)
)

all_invalid_values_examples = (
    [True, 1, 1.25, "2"],
    (True, 1, 1.25, "2"),
    [1, 2, 3, 4],
    (1, "2", 3, "4"),
    ("1", "2", "3", "4"),
    (1, 2, 3, 4),
)

all_invalid_values_examples_combinations = tuple(
    combo
    for r in range(1, len(all_invalid_values_examples) + 1)
    for combo in combinations(all_invalid_values_examples, r)
)


def test_no_arguments():
    @strict
    def foo():
        pass


def test_no_annotation():
    @strict
    def foo(a):
        pass


@pytest.mark.parametrize("allowed_type", allowed_types)
def test_valid_annotation(allowed_type):
    @strict
    def foo(a: allowed_type):
        pass


@pytest.mark.parametrize("invalid_type", INVALID_TYPES)
def test_invalid_annotation(invalid_type):
    with pytest.raises(TypeError):

        @strict
        def foo(a: invalid_type):
            pass


def test_type_var_annotation():
    T = TypeVar("T")

    @strict
    def foo(a: T):
        pass


@pytest.mark.parametrize("allowed_type", allowed_types)
def test_type_var_annotation_bound(allowed_type):
    T = TypeVar("T", bound=allowed_type)

    @strict
    def foo(a: T):
        pass


@pytest.mark.parametrize("allowed_types", type_var_constraints_combinations)
def test_type_var_annotation_constraints(allowed_types):
    T = TypeVar("T", *allowed_types)

    @strict
    def foo(a: T):
        pass


@pytest.mark.parametrize("invalid_type", INVALID_TYPES)
def test_type_var_annotation_bound_invalid(invalid_type):
    T = TypeVar("T", bound=invalid_type)

    with pytest.raises(TypeError):

        @strict
        def foo(a: T):
            pass


@pytest.mark.parametrize("invalid_types", type_var_constraints_combinations_invalid)
def test_type_var_annotation_constraints_invalid(invalid_types):
    T = TypeVar("T", *invalid_types)

    with pytest.raises(TypeError):

        @strict
        def foo(a: T):
            pass


def test_type_var_tuple_annotation():
    Ts = TypeVarTuple("Ts")

    @strict
    def foo(*args: *Ts):
        pass


def test_call_no_arguments():
    @strict
    def foo():
        pass

    foo()


@pytest.mark.parametrize(
    "allowed_value",
    tuple(element for sub_tuple in ALLOWED_EXAMPLES.values() for element in sub_tuple),
)
def test_call_no_annotation(allowed_value):
    @strict
    def foo(a):
        pass

    foo(allowed_value)


@pytest.mark.parametrize("allowed_type, allowed_value_tuple", ALLOWED_EXAMPLES.items())
def test_call_valid_annotation(allowed_type, allowed_value_tuple):
    @strict
    def foo(a: allowed_type):
        pass

    for allowed_value in allowed_value_tuple:
        foo(allowed_value)


@pytest.mark.parametrize("invalid_type", INVALID_TYPES)
def test_call_invalid_annotation(invalid_type):
    with pytest.raises(TypeError):

        @strict
        def foo(a: invalid_type):
            pass


@pytest.mark.parametrize("allowed_value_tuple", ALLOWED_EXAMPLES.values())
def test_call_type_var_annotation(allowed_value_tuple):
    T = TypeVar("T")

    @strict
    def foo(a: T):
        pass

    for allowed_value in allowed_value_tuple:
        foo(allowed_value)


@pytest.mark.parametrize("allowed_type, allowed_value_tuple", ALLOWED_EXAMPLES.items())
def test_call_type_var_annotation_bound(allowed_type, allowed_value_tuple):
    T = TypeVar("T", bound=allowed_type)

    @strict
    def foo(a: T):
        pass

    for allowed_value in allowed_value_tuple:
        foo(allowed_value)


@pytest.mark.parametrize("allowed_types", type_var_constraints_combinations)
def test_call_type_var_annotation_constraints(allowed_types):
    T = TypeVar("T", *allowed_types)

    @strict
    def foo(a: T):
        pass

    for allowed_type in allowed_types:
        for allowed_value in ALLOWED_EXAMPLES[allowed_type]:
            foo(allowed_value)


@pytest.mark.parametrize("invalid_value", INVALID_EXAMPLES.values())
def test_call_type_var_annotation_invalid(invalid_value):
    T = TypeVar("T")

    @strict
    def foo(a: T):
        pass

    with pytest.raises(TypeError):
        foo(invalid_value)


@pytest.mark.parametrize("allowed_type", ALLOWED_TYPES_BASE)
def test_call_type_var_annotation_bound_invalid(allowed_type):
    T = TypeVar("T", bound=allowed_type)

    @strict
    def foo(a: T):
        pass

    with pytest.raises(TypeError):
        for invalid_value in INVALID_EXAMPLES.values():
            foo(invalid_value)


@pytest.mark.parametrize("allowed_types", type_var_constraints_combinations)
def test_call_type_var_annotation_constraints_invalid(allowed_types):
    T = TypeVar("T", *allowed_types)

    @strict
    def foo(a: T):
        pass

    with pytest.raises(TypeError):
        for invalid_value in INVALID_EXAMPLES.values():
            foo(invalid_value)


@pytest.mark.parametrize(
    "allowed_value_tuple", all_allowed_values_examples_combinations
)
def test_call_type_var_tuple_annotation(allowed_value_tuple):
    Ts = TypeVarTuple("Ts")

    @strict
    def foo(*args: *Ts):
        pass

    foo(*allowed_value_tuple)


@pytest.mark.parametrize(
    "invalid_value_tuple", all_invalid_values_examples_combinations
)
def test_call_type_var_tuple_annotation_invalid(invalid_value_tuple):
    Ts = TypeVarTuple("Ts")

    @strict
    def foo(*args: *Ts):
        pass

    with pytest.raises(TypeError):
        foo(*invalid_value_tuple)
