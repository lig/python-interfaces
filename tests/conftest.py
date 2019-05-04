import pathlib
import sys
import typing

import pytest


def pytest_configure(config):
    sys.path.insert(0, str(pathlib.Path(__file__).parents[1]))


@pytest.fixture(scope='session')
def typeT1():
    return typing.TypeVar('T1')


@pytest.fixture(scope='session')
def typeT2():
    return typing.TypeVar('T2')
