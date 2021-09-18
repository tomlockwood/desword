import pytest

from desword.parsing.md import CustomMarkdownParser


@pytest.fixture
def markdown_parser():
    return CustomMarkdownParser('./generic/path/')


def test_regular_generation(markdown_parser):
    html, links = markdown_parser.generate_html_and_links('# Hi')
    assert len(links) == 0
    assert html == '<h1>Hi</h1>'


def test_link_generation(markdown_parser):
    _, links = markdown_parser.generate_html_and_links('# Hi\n[bbb](tengu)')
    assert len(links) == 1
    assert links[0] == {'href': './generic/path/tengu.html', 'text': 'bbb'}
