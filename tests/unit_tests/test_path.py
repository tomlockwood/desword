
def test_href_override(path_data):
    assert path_data.href_root == path_data.output
    path_data.href_override = 'www.exaample.com/butt/'
    assert path_data.href_root == path_data.href_override


def test_relative_location(path_data):
    assert path_data.relative_location(
        path_data.input, 'butt.md') == 'butt.md'
    assert path_data.relative_location(
        path_data.input + "/chonker", 'butt.md') == 'chonker/butt.md'
