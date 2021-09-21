import shutil
import os
from pathlib import Path


class FileHandler:
    def __init__(self, path):
        self.path = path
        self.empty_output()
        self.file_graph = {}
        self.other_files = []

    def empty_output(self):
        list_dir = os.listdir(self.path.output)
        for obj in list_dir:
            path = os.path.join(self.path.output, obj)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.unlink(path)

    def generate_file_graph(self):
        for root, _, files in os.walk(self.path.input):
            output_folder_full_path = self.path.output_folder_full_path(root)
            Path(output_folder_full_path).mkdir(parents=True, exist_ok=True)
            for file in files:
                # Ignore non-markdown files
                file_base, file_extension = self.path.file_parts(file)
                if file_extension != '.md':
                    self.other_files.append(file)
                    continue

                with open(os.path.join(root, file)) as f:
                    lines = f.read()

                relative_location = self.path.relative_location(
                    root, file_base)
                self.file_graph[relative_location] = {"lines": lines}
        return self.file_graph
