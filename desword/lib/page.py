class Page:
    def __init__(self, html, links):
        self.html = html
        self.links = links
        self.backlinks = {}

    def add_backlinks(self):
        for k, v in self.backlinks.items():
            self.html += f'\nFrom <a href="{k}">{k}</a> link: {v}'