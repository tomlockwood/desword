import os
import sys
from markdown import Markdown, inlinepatterns
import xml.etree.ElementTree as etree

input = sys.argv[1]

m = Markdown()

m.inlinePatterns.deregister('link')

class CustomLinkInlineProcessor(inlinepatterns.LinkInlineProcessor):
    def __init__(self, pattern, md):
        super().__init__(pattern, md=md)
        self.links = []

    def handleMatch(self, m, data):
        text, index, handled = self.getText(data, m.end(0))
        print(text)

        if not handled:
            return None, None, None

        href, title, index, handled = self.getLink(data, index)
        if not handled:
            return None, None, None

        el = etree.Element("a")
        el.text = text

        # Prepend input folder to link #FIXME
        link = input + href
        self.links.append((text, link))
        el.set("href", link)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index

m.inlinePatterns.register(CustomLinkInlineProcessor(inlinepatterns.LINK_RE, m), 'link', 160)

for root, _, files in os.walk(input):
    for file in files:
        with open(os.path.join(root, file)) as f:
            lines = f.read()
        print(m.convert(lines))
        print(m.inlinePatterns['link'].links)