from desword.site_generator import SiteGenerator
import os
import pytest


@pytest.fixture
def site_generator(temp_in_out_dirs):
    yield SiteGenerator(temp_in_out_dirs['in'], temp_in_out_dirs['out'])


def test_site_generator_blank(site_generator):
    assert site_generator.missing_pages == []
    assert site_generator.file_graph == {}


def test_site_generator_no_markdown_file(site_generator):
    with open(os.path.join(site_generator.path_data.output, "example.txt"), "w") as f:
        f.write('Invalid file')
    assert site_generator.missing_pages == []
    assert site_generator.file_graph == {}


def test_add_page_to_graph(site_generator):
    site_generator.file_graph = {"a": {"lines": " # Hi"}}
    site_generator.add_pages_to_graph()
    assert site_generator.file_graph['a'].get('page')
