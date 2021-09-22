import lib


class SiteGenerator:
    def __init__(self, input, output, href_base=None, page_template_path=None):
        self.path_data = lib.PathData(input, output, href_base)
        self.file_handler = lib.FileHandler(self.path_data)
        self.markdown_parser = lib.CustomMarkdownParser(self.path_data)
        if not page_template_path:
            page_template_path = 'desword/templates/page.html'

        with open(page_template_path) as f:
            self.page_template = f.read()

        self.missing_pages = []

        self.file_graph = self.file_handler.generate_file_graph()

        self.add_pages_to_graph()

        self.record_link_edges()

        self.output_html()

    def add_pages_to_graph(self):
        # Parse Markdown to generate HTML and links on pages
        for k, v in self.file_graph.items():
            body, links = self.markdown_parser.generate_html_and_links(
                v['lines'])
            self.file_graph[k]['page'] = lib.Page(
                body, links, self.page_template)

    def record_link_edges(self):
        # For every node in the file_graph...
        for source, node in self.file_graph.items():
            # For every link in that node's page...
            for link in node['page'].links:
                # If the file_graph doesn't contain a target for the link..
                if not self.file_graph.get(link["rel"]):
                    # Add the target to missing pages...
                    self.missing_pages.append(link)
                    continue

                # Otherwise add on the target page information about where it is
                # being linked to, from!
                self.file_graph[link["rel"]
                                ]["page"].backlinks[self.path_data.href(source)] = link

    def output_html(self):
        # Add backlinks to html and output finished HTML to filesystem
        for out, node in self.file_graph.items():
            node["page"].generate_html()
            self.file_handler.write_page(out, node["page"])
