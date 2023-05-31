from check_file_and_directory_names import core

def main():
    file_tree = core.FileTree()
    for path in core.get_added_filepaths():
        file_tree.add_path_to_tree(path, path.is_file())
    upper_case_dirpaths = list(
        file_tree.iterate_over_directory_names(
            filter_func=lambda dir_name: not dir_name.islower()  # type: ignore
        )
    )
    upper_case_filepaths = list(
        file_tree.iterate_over_file_names(
            filter_func=lambda dir_name: not dir_name.islower()  # type: ignore
        )
    )
    ret = 0
    if (len(upper_case_filepaths) != 0) or (len(upper_case_dirpaths) != 0):
        ret = 1
    return ret

if __name__ == "__main__":
    ret = main()
    raise SystemExit(ret)

