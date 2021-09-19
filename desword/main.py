import os
import sys
from md import CustomMarkdownParser
from file_handler import FileHandler
from pathlib import Path

input = sys.argv[1]
output = sys.argv[2]

f = FileHandler(input, output)

m = CustomMarkdownParser(output)


class Page:
    def __init__(self, html, links):
        self.html = html
        self.links = links
        self.backlinks = {}

    def add_backlinks(self):
        for k, v in self.backlinks.items():
            self.html += f'\nFrom <a href="{k}">{k}</a> link: {v}'


f.generate_file_lists()

for k, v in f.page_graph.items():

    html, links = m.generate_html_and_links(v['lines'])
    f.page_graph[k]['page'] = Page(html, links)

missing_pages = []

for out, node in f.page_graph.items():
    for link in node['page'].links:
        if not f.page_graph.get(link["href"]):
            missing_pages.append(link)
            continue

        f.page_graph[link["href"]]["page"].backlinks[out] = link

for out, node in f.page_graph.items():
    node["page"].add_backlinks()
    with open(out, "w") as f:
        f.write(node["page"].html)
