class Page:
    def __init__(self, body, links, template):
        self.body = body
        self.links = links
        self.template = template
        self.backlinks = {}

    def add_backlinks(self):
        for k, v in self.backlinks.items():
            self.body += f'\nFrom <a href="{k}">{k}</a> link: {v}'

    def generate_html(self):
        self.add_backlinks()
        self.html = self.template % (self.body)
