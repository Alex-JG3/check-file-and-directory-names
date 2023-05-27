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


if __name__ == "__main__":
    added_filepaths = get_added_filepaths()
    upper_case_filepaths = get_paths_with_uppercase_in_filename(added_filepaths)
    upper_case_dirpaths = get_paths_with_uppercase_in_dirname(added_filepaths)  
    ret = 0
    if (len(upper_case_filepaths) != 0) or (len(upper_case_dirpaths) != 0):
        ret = 1
    raise SystemExit(ret)

