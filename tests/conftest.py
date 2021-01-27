# content of conftest.py
import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--token", action="store", help="JWT Token"
    )


@pytest.fixture
def token(request):
    return request.config.getoption("--token")
