import glob
import os
import sys
from parsing.md import CustomMarkdownParser

input = sys.argv[1]
output = sys.argv[2]

if not output.strip():
    raise Exception('Output blank')

files = glob.glob(f"{output}*")
for f in files:
    os.remove(f)

m = CustomMarkdownParser(output)

page_graph = {}


class Page:
    def __init__(self, m, lines):
        self.html, self.links = m.generate_html_and_links(lines)
        self.backlinks = {}

    def add_backlinks(self):
        for k, v in self.backlinks.items():
            self.html += f'\nFrom <a href="{k}">{k}</a> link: {v}'


for root, _, files in os.walk(input):
    for file in files:
        file_parts = os.path.splitext(file)
        # Ignore non-markdown files
        if file_parts[1] != '.md':
            # Maybe move the static files into the same folder?
            continue

        input_location = os.path.join(root, file)
        output_location = os.path.join(output, file_parts[0] + ".html")
        with open(input_location) as f:
            lines = f.read()
        page_graph[output_location] = Page(m, lines)

missing_pages = []

for out, page in page_graph.items():
    for link in page.links:
        if not page_graph.get(link["href"]):
            missing_pages.append(link)
            continue

        page_graph[link["href"]].backlinks[out] = link

for out, page in page_graph.items():
    page.add_backlinks()
    with open(out, "w") as f:
        f.write(page.html)
