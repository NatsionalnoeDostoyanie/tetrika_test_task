import pytest

from task2.solution import _extend_letters_to_animals_count


def test_extend_letters_to_animals_count():
    counter = {"A": 0, "B": 0}
    names = ("Apple", "Banana", "Ant")
    _extend_letters_to_animals_count(counter, names)
    assert counter["A"] == 2
    assert counter["B"] == 1


def test_extend_letters_to_animals_count_invalid():
    counter = {"A": 0}
    names = ["123Test", "", "Apple", "Y"]
    _extend_letters_to_animals_count(counter, names)
    with pytest.raises(AssertionError):
        assert counter["A"] != 1


def test_extend_letters_to_animals_count_empty_names():
    counter = {"A": 0}
    names = []
    _extend_letters_to_animals_count(counter, names)
    assert counter["A"] == 0
