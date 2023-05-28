from check_file_and_directory_names import core

def main():
    added_filepaths = core.get_added_filepaths()
    upper_case_filepaths = core.get_paths_with_uppercase_in_filename(added_filepaths)
    directory_tree = core.create_directory_tree(added_filepaths)
    upper_case_dirpaths = list(
        core.directory_name_iter(
            directory_tree,
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

