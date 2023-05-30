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

@pytest.fixture(scope="session")
def file_tree():
    file_tree = core.FileTree()
    file_tree.add_path_to_tree(pathlib.Path("dir1") / "file1.py", is_file_path=True)
    file_tree.add_path_to_tree(pathlib.Path("dir1") / "subdir1" / "file2.py", is_file_path=True)
    file_tree.add_path_to_tree(pathlib.Path("dir1") / "subdir1" / "file1.py", is_file_path=True)
    return file_tree

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

def test_add_path_to_file_tree(file_tree):
    assert file_tree["dir1"].files == ["file1.py"]
    assert set(file_tree["dir1"]["subdir1"].files) == {"file1.py", "file2.py"}

def test_iterate_over_directory_names(file_tree):
    dir_names = set()
    expected_dir_names = {"dir1", "subdir1"}
    for dir_name, _ in file_tree.iterate_over_directory_names():
        dir_names.add(dir_name)
    assert dir_names == expected_dir_names

def test_iterate_over_file_names(file_tree):
    filenames = set()
    expected_filenames = {"file1.py", "file2.py"}
    for filename, _ in file_tree.iterate_over_file_names():
        filenames.add(filename)
    assert filenames == expected_filenames

