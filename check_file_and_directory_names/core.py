import subprocess
from pathlib import Path


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
            add_path_parts_to_directory_tree(path.parent.parts, directory_tree)
        else:
            add_path_parts_to_directory_tree(path.parts, directory_tree)
    return directory_tree

def directory_name_iter(directory_tree, parents=[], filter_func=lambda _: True):
    for dir_name, sub_tree in directory_tree.items():
        if filter_func(dir_name):
            yield dir_name, parents
        if sub_tree != {}:
            yield from directory_name_iter(sub_tree, parents + [dir_name], filter_func)
