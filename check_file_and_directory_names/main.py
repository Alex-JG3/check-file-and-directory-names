from check_file_and_directory_names import core

def main():
    file_tree = core.FileTree()
    for path in core.get_added_filepaths():
        file_tree.add_path_to_tree(path, path.is_file())
    checkers = [
        core.CapitalLetterChecker()
    ]
    file_tree.run_checkers_over_tree(checkers)
    ret = 0
    for checker in checkers:
        if len(checker.flagged_paths) != 0:
            ret = 1
    return ret

if __name__ == "__main__":
    ret = main()
    raise SystemExit(ret)

