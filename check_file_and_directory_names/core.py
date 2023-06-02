import subprocess
from pathlib import Path
from collections import UserDict
from abc import ABC, abstractmethod
from typing import List, Tuple


class Checker(ABC):
    @abstractmethod
    def check_name(self, name, parent_parts):
        pass

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

    def iterate_over_directory_names(self,  filter_func=None, parent_parts=None):
        if parent_parts is None:
            parent_parts = []
        for dir_name, subtree in self.items():
            yield from subtree.iterate_over_directory_names(
                filter_func, parent_parts + [dir_name]
            )
            if filter_func is None:
                yield dir_name, parent_parts
            elif filter_func(dir_name):
                yield dir_name, parent_parts

    def iterate_over_file_names(self, filter_func=None, parent_parts=None):
        if parent_parts is None:
            parent_parts = []
        for dir_name, subtree in self.items():
            yield from subtree.iterate_over_file_names(
                filter_func, parent_parts + [dir_name]
            )
        for filename in self.files:
            if filter_func is None:
                yield filename, parent_parts
            elif filter_func(filename):
                yield filename, parent_parts

    def run_checkers_over_tree(self, checkers: List):
        for dir_name, parent_parts in self.iterate_over_directory_names():
            for checker in checkers:
                checker.check_name(dir_name, parent_parts)
        for file_name, parent_parts in self.iterate_over_file_names():
            for checker in checkers:
                checker.check_name(file_name, parent_parts)

class CapitalLetterChecker(Checker):
    def __init__(self):
        self.string_reference = "These file and directory names contain capital letters:"
        self.flagged_paths = []

    def check_name(self, name: str, parent_parts: Tuple[str]):
        if not name.islower():
            self.flagged_paths.append(Path(*parent_parts) / name)

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
