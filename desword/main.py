import glob
import os
import sys
from markdown import Markdown, inlinepatterns
import xml.etree.ElementTree as etree

input = sys.argv[1]
output = sys.argv[2]

if not output.strip():
    raise Exception('Output blank')

files = glob.glob(f"{output}*")
for f in files:
    os.remove(f)

m = Markdown()

m.inlinePatterns.deregister('link')

class CustomLinkInlineProcessor(inlinepatterns.LinkInlineProcessor):
    def __init__(self, pattern, md):
        super().__init__(pattern, md=md)

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("a")
        el.text = text

        # Prepend output folder path (or url) to link
        link = output + href + ".html"
        self.links.append({"text": text, "href": link})
        el.set("href", link)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index

m.inlinePatterns.register(CustomLinkInlineProcessor(inlinepatterns.LINK_RE, m), 'link', 160)

page_graph = {}

class Page:
    def __init__(self, m, lines):
        m.inlinePatterns['link'].links = []
        self.html = m.convert(lines)
        self.links = m.inlinePatterns['link'].links
        self.backlinks = {}

for root, _, files in os.walk(input):
    for file in files:
        file_parts = os.path.splitext(file)
        # Ignore non-markdown files
        if file_parts[1] != '.md':
            # Maybe move the static files into the same folder?
            continue

        # Clear links array
        m.inlinePatterns['link'].links = []
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
    for k, v in page.backlinks.items():
        page.html += f"\nFrom {k} link: {v}"
    with open(out, "w") as f:
        f.write(page.html)