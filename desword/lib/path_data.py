import os


class PathData:
    def __init__(self, input_path, output_path, path_for_href=None):
        self.input = input_path
        self.output = output_path
        self.href_override = path_for_href

    def validate_path_string(self, val):
        if not val.strip():
            raise Exception('Output blank')

        if not val[-1] == os.path.sep:
            val = f"{val}{os.path.sep}"
        return val

    # Properties
    @property
    def input(self):
        return self._input

    @input.setter
    def input(self, val):
        self._input = self.validate_path_string(val)

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, val):
        self._output = self.validate_path_string(val)

    @property
    def href_root(self):
        return self.href_override or self.output

    def href(self, href):
        return f"{self.href_root}{href}.html"

    # Returns relative subdirectory structure (if any) for a given path
    def relative_import_folder(self, root):
        input_relative_path = os.path.relpath(
            root, self.input)
        if input_relative_path == ".":
            return
        return input_relative_path

    def relative_location(self, root, file_base):
        path_args = []
        relative_import = self.relative_import_folder(root)
        if relative_import:
            path_args.append(relative_import)
        path_args.append(file_base)
        return os.path.join(*path_args)

    # Returns full path of folder in output location
    def output_folder_full_path(self, root):
        path_args = [self.output]
        relative_import = self.relative_import_folder(root)
        if relative_import:
            path_args.append(relative_import)
        return os.path.join(*path_args)

    def output_file_location(self, relative_location):
        return os.path.join(self.output, relative_location + '.html')

    def file_parts(self, filename):
        split = os.path.splitext(filename)
        return split[0], split[1]
