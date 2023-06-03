import os
import subprocess
import pathlib

import pytest

from check_file_and_directory_names import main

@pytest.fixture(scope="session")
def git_repo_path_no_issues(tmpdir_factory):
    git_repo_path = tmpdir_factory.mktemp("git_repo_no_issues")
    git_repo_path = pathlib.Path(git_repo_path)
    os.chdir(git_repo_path)
    subprocess.run(["git", "init"])
    (git_repo_path / "dir").mkdir()
    (git_repo_path / "dir" / "file1").touch()
    (git_repo_path / "file2").touch()
    subprocess.run(["git", "add", "."])
    return git_repo_path

@pytest.fixture(scope="session")
def git_repo_path_with_issues(tmpdir_factory):
    git_repo_path = tmpdir_factory.mktemp("git_repo_with_issues")
    git_repo_path = pathlib.Path(git_repo_path)
    os.chdir(git_repo_path)
    subprocess.run(["git", "init"])
    (git_repo_path / "Dir").mkdir()
    (git_repo_path / "Dir" / "file1").touch()
    (git_repo_path / "File2").touch()
    subprocess.run(["git", "add", "."])
    return git_repo_path

def test_main_no_issues(git_repo_path_no_issues):
    os.chdir(git_repo_path_no_issues)
    parser = main.create_parser()
    args = parser.parse_args(["--no_capital_letters", "--illegal_characters", "-"])
    assert main.main(args) == 0

def test_main_with_issues(git_repo_path_with_issues):
    os.chdir(git_repo_path_with_issues)
    parser = main.create_parser()
    args = parser.parse_args(["--no_capital_letters", "--illegal_characters", "-"])
    assert main.main(args) == 1

