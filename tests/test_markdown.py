import pytest

from desword.parsing.md import CustomMarkdownParser


@pytest.fixture
def markdown_parser():
    return CustomMarkdownParser('./generic/path')


def test_links_generation(markdown_parser):
    html, links = markdown_parser.generate_html_and_links('Hi')
    assert len(links) == 0
    assert html == '<p>Hi</p>'
