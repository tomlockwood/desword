import glob
import os
import sys
from md import CustomMarkdownParser
from pathlib import Path

input = sys.argv[1]
output = sys.argv[2]

if not output.strip():
    raise Exception('Output blank')

if not output[-1] == os.path.sep:
    output = f"{output}{os.path.sep}"

files = glob.glob(f"{output}*")
print(files)
directories = []
for f in files:
    if not os.path.isfile(f):
        directories.append(f)
    else:
        os.remove(f)

for d in directories:
    os.rmdir(d)

m = CustomMarkdownParser(output)

page_graph = {}


class Page:
    def __init__(self, m, lines):
        self.html, self.links = m.generate_html_and_links(lines)
        self.backlinks = {}

    def add_backlinks(self):
        for k, v in self.backlinks.items():
            self.html += f'\nFrom <a href="{k}">{k}</a> link: {v}'


for root, dirs, files in os.walk(input):
    input_relative_path = os.path.relpath(
        root, input)
    output_relative_path = os.path.join(
        output, input_relative_path)
    Path(output_relative_path).mkdir(parents=True, exist_ok=True)
    for file in files:
        file_parts = os.path.splitext(file)
        # Ignore non-markdown files
        if file_parts[1] != '.md':
            # Maybe move the static files into the same folder?
            continue

        input_location = os.path.join(root, file)
        output_location = os.path.join(
            output_relative_path, file_parts[0] + ".html")
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
