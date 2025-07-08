import pytest

def pytest_addoption(parser):
    parser.addoption("--file")

@pytest.fixture
def cmdopt(request):
    return request.config.getoption("--file")