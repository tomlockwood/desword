import pytest
import tempfile

from desword.md import CustomMarkdownParser


@pytest.fixture
def temp_dir():
    tmp = tempfile.TemporaryDirectory()
    yield tmp.name + "/"
    tmp.cleanup()


@pytest.fixture
def markdown_parser(temp_dir):
    return CustomMarkdownParser(temp_dir)


def test_regular_generation(markdown_parser):
    html, links = markdown_parser.generate_html_and_links('# Hi')
    assert len(links) == 0
    assert html == '<h1>Hi</h1>'


def test_link_generation(markdown_parser):
    _, links = markdown_parser.generate_html_and_links('# Hi\n[bbb](tengu)')
    assert len(links) == 1
    assert links[0] == {
        'href': f'{markdown_parser.output_path}tengu.html', 'text': 'bbb'}
