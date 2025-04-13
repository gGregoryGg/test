import pytest

from utils import (
    get_batches,
    get_info,
)


def test_empty_list():
    assert get_batches([]) == []


def test_single_element_batch_size_1():
    assert get_batches([1], 1) == [[1]]


def test_single_element_batch_size_2():
    assert get_batches([1], 2) == [[1]]


def test_multiple_elements_batch_size_2():
    assert get_batches([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_multiple_elements_batch_size_3():
    assert get_batches([1, 2, 3, 4, 5], 3) == [[1, 2, 3], [4, 5]]


def test_string_input():
    assert get_batches("abcdef", 2) == [["a", "b"], ["c", "d"], ["e", "f"]]


def test_tuple_input():
    assert get_batches((1, 2, 3, 4), 2) == [[1, 2], [3, 4]]


def test_batch_size_larger_than_input():
    assert get_batches([1, 2, 3], 5) == [[1, 2, 3]]


def test_batch_size_equal_to_input_length():
    assert get_batches([1, 2, 3], 3) == [[1, 2, 3]]


def test_zero_batch_size():
    with pytest.raises(ValueError):
        get_batches([1, 2, 3], 0)


def test_negative_batch_size():
    with pytest.raises(ValueError):
        get_batches([1, 2, 3], -1)


def test_valid_django_request_with_url():
    line = "2023-01-01 12:00:00 INFO django.request: GET /api/users"
    assert get_info(line) == ("INFO", "/api/users")


def test_valid_django_request_without_url():
    line = "2023-01-01 12:00:00 INFO django.request: Some message"
    assert get_info(line) is None


def test_non_django_request_line():
    line = "2023-01-01 12:00:00 INFO other.module: GET /api/users"
    assert get_info(line) is None


def test_empty_line():
    line = ""
    assert get_info(line) is None


def test_url_but_not_django_request():
    line = "2023-01-01 12:00:00 INFO other.module: GET /api/users"
    assert get_info(line) is None


def test_url_in_different_position():
    line = "2023-01-01 12:00:00 INFO django.request: Some /path message"
    assert get_info(line) == ("INFO", "/path")


def test_line_with_tab_separator():
    line = "2023-01-01\t12:00:00\tINFO\tdjango.request:\tGET\t/api/users"
    assert get_info(line) == ("INFO", "/api/users")


def test_line_with_extra_spaces():
    line = "  2023-01-01  12:00:00  INFO  django.request:  GET  /api/users  "
    assert get_info(line) == ("INFO", "/api/users")
