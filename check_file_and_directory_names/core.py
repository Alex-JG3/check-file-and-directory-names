import subprocess
from pathlib import Path
from collections import UserDict


class FileTree(UserDict):
    def __init__(self):
        super(FileTree, self).__init__()
        self.files = []

    def add_path_to_tree(self, path: Path, is_file_path: bool):
        if is_file_path:
            self.add_parts_to_tree(path.parts[:-1], path.parts[-1])
        else:
            self.add_parts_to_tree(path.parts)

    def add_parts_to_tree(self, dir_parts, file_part=None):
        if len(dir_parts) == 0:
            if file_part is not None:
                self.files.append(file_part)
        else:
            if dir_parts[0] not in self:
                self.__setitem__(dir_parts[0], FileTree())
            self.__getitem__(dir_parts[0]).add_parts_to_tree(dir_parts[1:], file_part)

def get_added_filepaths():
    added_filepaths = subprocess.run(
        ['git', '--no-pager', 'diff', '--cached', '--name-only', '--diff-filter=A'],
        stdout=subprocess.PIPE
    ).stdout.decode("utf-8")
    added_filepaths = added_filepaths.splitlines()
    added_filepaths = [Path(path) for path in added_filepaths]
    return added_filepaths

def get_paths_with_uppercase_in_filename(paths):
    return [p for p in paths if not p.stem.islower()]

def get_paths_with_uppercase_in_dirname(paths):
    paths_with_uppercase_in_dirname = []
    for path in paths:
        # Remove filename, we are only interested in directory names here
        if path.is_file():
            path = path.parent
        if not "".join(path.parts).islower():
            paths_with_uppercase_in_dirname.append(path)
    return paths_with_uppercase_in_dirname

def add_path_parts_to_directory_tree(path_parts, directory_tree):
    if path_parts[0] not in directory_tree:
        directory_tree[path_parts[0]] = {}

    if len(path_parts) == 1:
        return
    else:
        add_path_parts_to_directory_tree(
            path_parts[1:],
            directory_tree[path_parts[0]]
        )

def create_directory_tree(paths):
    directory_tree = {}
    for path in paths:
        if path.is_file():
            path = path.parent
        if path.parts != ():
            add_path_parts_to_directory_tree(path.parts, directory_tree)
    return directory_tree

def directory_name_iter(directory_tree, parents=[], filter_func=lambda _: True):
    for dir_name, sub_tree in directory_tree.items():
        if filter_func(dir_name):
            yield dir_name, parents
        if sub_tree != {}:
            yield from directory_name_iter(sub_tree, parents + [dir_name], filter_func)
