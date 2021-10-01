import lib


class SiteGenerator:
    def __init__(self, input, output, href_base=None, page_template_path=None):
        self.path_data = lib.Path(input, output, href_base)
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

        self.output_files()

    def add_pages_to_graph(self):
        # Parse Markdown to generate HTML and links on pages
        for source, node in self.file_graph.items():
            if not node['path'].is_markdown:
                continue
            body, links = self.markdown_parser.generate_html_and_links(
                node)
            self.file_graph[source]['page'] = lib.Page(
                body, links, self.page_template)

    def record_link_edges(self):
        # For every node in the file_graph...
        for _, node in self.file_graph.items():
            if not node['path'].is_markdown:
                continue
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
                                ]["page"].backlinks[node["path"].href] = link

    def output_files(self):
        # TODO: System pages aka missing pages
        # TODO: Page categories/metadata (main pages for subfolders)
        # Add backlinks to html and output finished HTML to filesystem
        for _, node in self.file_graph.items():
            if node["path"].is_markdown:
                node["page"].generate_html()
            self.file_handler.write(node)
