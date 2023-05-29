import os
import subprocess
import pathlib

import pytest

from check_file_and_directory_names import core

@pytest.fixture(scope="session")
def git_repo_path(tmpdir_factory):
    git_repo_path = tmpdir_factory.mktemp("git_repo")
    git_repo_path = pathlib.Path(git_repo_path)
    os.chdir(git_repo_path)
    subprocess.run(["git", "init"])
    (git_repo_path / "dir").mkdir()
    (git_repo_path / "dir" / "file1").touch()
    (git_repo_path / "file2").touch()
    subprocess.run(["git", "add", "."])
    return git_repo_path

def test_get_added_filepaths(git_repo_path):
    os.chdir(git_repo_path)
    added_filepaths = core.get_added_filepaths()
    expected_added_filepaths = [
        pathlib.Path("dir") / "file1",
        pathlib.Path("file2"),
    ]
    # The order is not important so we change to sets first
    assert set(added_filepaths) == set(expected_added_filepaths)

def test_create_directory_tree(git_repo_path):
    os.chdir(git_repo_path)
    added_filepaths = core.get_added_filepaths()
    directory_tree = core.create_directory_tree(added_filepaths)
    assert directory_tree.keys() == {"dir"}
    assert directory_tree["dir"] == {}

def test_check_for_dirnames_with_capitals():
    paths = [
        pathlib.Path("dir1") / "file1",
        pathlib.Path("Dir2") / "file2",
        pathlib.Path("Dir2") / "Subdir1" / "file2",
    ]
    directory_tree = core.create_directory_tree(paths)
    dirs_with_capitals = list(
        core.directory_name_iter(
            directory_tree, filter_func=lambda dirname: not dirname.islower()  # type: ignore
        )
    )
    assert len(dirs_with_capitals) == 2

