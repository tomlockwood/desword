from desword.lib import Page


def test_backlinks():
    p = Page('<p>Nothing</p>', None)
    p.backlinks = {"k": {"usually": "a link"}}
    p.add_backlinks()
    assert p.html == '''
    <p>Nothing</p>\nFrom <a href="k">k</a> link: {'usually': 'a link'}
    '''.strip()
