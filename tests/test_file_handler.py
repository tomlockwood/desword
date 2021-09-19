from desword.file_handler import FileHandler
import os
import pytest


def test_adding_separator(temp_in_out_dirs):
    f = FileHandler(temp_in_out_dirs['in'], temp_in_out_dirs['out'])
    assert f.output_path == temp_in_out_dirs['out'] + os.path.sep


def test_blank_output(temp_in_out_dirs):
    with pytest.raises(Exception):
        FileHandler(temp_in_out_dirs['in'], "")


def test_file_cleaned(temp_in_out_dirs):
    internal_directory = os.path.join(temp_in_out_dirs['out'], 'depth')
    os.mkdir(internal_directory)
    with open(os.path.join(internal_directory, "example.md"), "w") as f:
        f.write('<h1>Hallo</h1>')
    assert os.listdir(internal_directory) == ['example.md']
    f = FileHandler(temp_in_out_dirs['in'], temp_in_out_dirs['out'])
    f.empty_output()
    assert os.listdir(temp_in_out_dirs['out']) == []
