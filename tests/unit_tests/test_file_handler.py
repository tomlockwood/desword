from desword.file_handler import FileHandler
import os


def test_file_cleaned(path_data):
    internal_directory = os.path.join(path_data.output, 'depth')
    os.mkdir(internal_directory)
    with open(os.path.join(internal_directory, "example.md"), "w") as f:
        f.write('<h1>Hallo</h1>')
    assert os.listdir(internal_directory) == ['example.md']
    f = FileHandler(path_data)
    f.empty_output()
    assert os.listdir(path_data.output) == []
