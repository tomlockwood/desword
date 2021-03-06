
import os
import pytest
import tempfile
import sys
sys.path.append("desword")


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


@pytest.fixture
def path_data(temp_in_out_dirs):
    from lib import Path
    yield Path(temp_in_out_dirs['in'], temp_in_out_dirs['out'])
