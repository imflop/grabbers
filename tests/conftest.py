import pytest

from grabbers.hh.app import create_app


@pytest.fixture
def app():
    app = create_app()
    yield app
    app.container.unwire()
