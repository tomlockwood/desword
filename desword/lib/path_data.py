import os


class File:
    def __init__(self, path, root, file):
        self.path = path
        self.root = root
        self.file = file
        self.initialize()

    def initialize(self):
        self.file_parts = os.path.splitext(self.file)
        self._input_path = os.path.join(self.root, self.name)
        self._relative_path = os.path.relpath(
            self._input_path, self.path.input)

    @ property
    def input_path(self):
        return self._input_path + self.extension

    @ property
    def is_markdown(self):
        return self.extension == '.md'

    @property
    def output_file(self):
        if self.is_markdown:
            ext = '.html'
        else:
            ext = self.extension
        return self.relative_path + ext

    @ property
    def output_path(self):
        return os.path.join(self.path.output, self.output_file)

    @ property
    def relative_path(self):
        if self._relative_path == ".":
            return
        return self._relative_path

    @ property
    def output_folder(self):
        input_relative_path = os.path.relpath(
            self.root, self.path.input)
        if input_relative_path == ".":
            return self.path.output
        return os.path.join(self.path.output, input_relative_path)

    @ property
    def file_parts(self):
        return self._file_parts

    @ file_parts.setter
    def file_parts(self, val):
        self._file_parts = val
        self.name = val[0]
        self.extension = val[1]

    @property
    def href(self):
        return f"{self.path.href_root}{self.output_file}"


class Path:
    def __init__(self, input_path, output_path, path_for_href=None):
        self.input = input_path
        self.output = output_path
        self.href_override = path_for_href

    def file(self, root, file):
        return File(self, root, file)

    def validate_path_string(self, val):
        if not val.strip():
            raise Exception('Path blank.')

        if not val[-1] == os.path.sep:
            val = f"{val}{os.path.sep}"
        return val

    # Properties
    @ property
    def input(self):
        return self._input

    @ input.setter
    def input(self, val):
        self._input = self.validate_path_string(val)

    @ property
    def output(self):
        return self._output

    @ output.setter
    def output(self, val):
        self._output = self.validate_path_string(val)

    @ property
    def href_root(self):
        return self.href_override or self.output

    def href(self, href):
        # FIXME: Only add html to relative links
        # Where markdown parser generates arbitrary links from [link text](href/path)
        # type links
        return f"{self.href_root}{href}.html"
