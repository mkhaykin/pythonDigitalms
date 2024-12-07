from unittest.mock import patch

from pytest_mock import MockerFixture
from task2 import solve


@patch("task2.isBrokenVersion", new=lambda n: n >= 5)
def test_solve_5() -> None:
    assert solve(10**100) == 5


def test_solve_1(mocker: MockerFixture) -> None:
    mocker.patch("task2.isBrokenVersion", return_value=True)
    assert solve(10**100) == 1


def test_solve_inf(mocker: MockerFixture) -> None:
    mocker.patch("task2.isBrokenVersion", return_value=False)
    assert solve(10**100) == 10**100
