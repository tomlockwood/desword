import os
import pytest
import tempfile


@pytest.fixture
def temp_dir():
    tmp = tempfile.TemporaryDirectory()
    yield tmp.name + "/"
    tmp.cleanup()


@pytest.fixture
def temp_in_out_dirs(temp_dir):
    in_path = os.path.join(temp_dir, 'in')
    out_path = os.path.join(temp_dir, 'out')
    os.mkdir(in_path)
    os.mkdir(out_path)
    yield {"in": in_path, "out": out_path}
