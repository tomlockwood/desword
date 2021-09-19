import shutil
import os
from pathlib import Path


class FileHandler:
    def __init__(self, input_path, output_path):
        self.output_path = output_path
        self.empty_output()
        self.input_path = input_path

    @property
    def output_path(self):
        return self._output

    @output_path.setter
    def output_path(self, val):
        if not val.strip():
            raise Exception('Output blank')

        if not val[-1] == os.path.sep:
            val = f"{val}{os.path.sep}"
        self._output = val

    def empty_output(self):
        list_dir = os.listdir(self.output_path)
        for obj in list_dir:
            path = os.path.join(self.output_path, obj)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    def generate_file_lists(self):
        self.page_graph = {}
        self.other_files = []
        for root, _, files in os.walk(self.input_path):
            input_relative_path = os.path.relpath(
                root, self.input_path)
            if not input_relative_path == ".":
                output_relative_path = os.path.join(
                    self.output_path, input_relative_path)
            else:
                output_relative_path = os.path.join(self.output_path)
            Path(output_relative_path).mkdir(parents=True, exist_ok=True)
            for file in files:
                file_parts = os.path.splitext(file)

                # Ignore non-markdown files
                if file_parts[1] != '.md':
                    self.other_files.append(file)
                    continue

                input_location = os.path.join(root, file)
                output_location = os.path.join(
                    output_relative_path, file_parts[0] + ".html")
                with open(input_location) as f:
                    lines = f.read()

                self.page_graph[output_location] = {
                    "input": input_location, "lines": lines}
