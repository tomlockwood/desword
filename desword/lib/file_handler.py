import shutil
import os
from pathlib import Path


class FileHandler:
    def __init__(self, path_data):
        self.path = path_data
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
            for file in files:
                file_path = self.path.file(root, file)
                node = {"file": file_path}
                # Ignore non-markdown files
                if file_path.is_markdown:
                    with open(os.path.join(root, file)) as f:
                        node["lines"] = f.read()

                self.file_graph[file_path.relative_path] = node
        return self.file_graph

    def write(self, node):
        node_file = node["file"]
        Path(node_file.output_folder).mkdir(parents=True, exist_ok=True)
        if node_file.is_markdown:
            with open(node_file.output_path, "w") as f:
                f.write(node["page"].html)
        else:
            shutil.copy(node_file.input_path, node_file.output_path)
