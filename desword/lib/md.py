from markdown import Markdown, inlinepatterns
import xml.etree.ElementTree as etree


class CustomLinkInlineProcessor(inlinepatterns.LinkInlineProcessor):
    def __init__(self, pattern, md, path):
        super().__init__(pattern, md=md)
        self.path = path

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
        link = self.path.href(href)
        self.links.append({"text": text, "href": link, "rel": href})
        el.set("href", link)

        if title is not None:
            el.set("title", title)

        return el, m.start(0), index


class CustomMarkdownParser:

    def __init__(self, path):
        self.markdown = Markdown()
        self.path = path
        self.markdown.inlinePatterns.deregister('link')
        self.markdown.inlinePatterns.register(CustomLinkInlineProcessor(
            inlinepatterns.LINK_RE, self.markdown, path), 'link', 160)

    def generate_html_and_links(self, node):
        self.markdown.inlinePatterns['link'].links = []
        html = self.markdown.convert(node['lines'])
        links = self.markdown.inlinePatterns['link'].links
        return html, links
