
def test_href_override(path_data):
    assert path_data.href_root == path_data.output
    path_data.href_override = 'www.exaample.com/butt/'
    assert path_data.href_root == path_data.href_override


def test_relative_path(path_data):
    file_path = path_data.file_path(
        path_data.input, 'butt.md')
    assert file_path.relative_path == 'butt'
    file_path = path_data.file_path(
        path_data.input + "/chonker", 'butt.md')
    assert file_path.relative_path == 'chonker/butt'
