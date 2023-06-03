import argparse

from check_file_and_directory_names import core

def main(args=None):
    file_tree = core.FileTree()
    for path in core.get_added_filepaths():
        file_tree.add_path_to_tree(path, path.is_file())
    checkers = []
    if args is not None and args.no_capital_letters:
        checkers.append(core.CapitalLetterChecker())
    if args is not None and len(args.illegal_characters) != 0:
        checkers.append(core.IllegalCharacterChecker(args.illegal_characters))

    file_tree.run_checkers_over_tree(checkers)
    ret = 0
    for checker in checkers:
        if len(checker.flagged_paths) != 0:
            core.print_output_from_checkers(checkers)
            ret = 1
            break
    return ret

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_capital_letters", action="store_true", default=False)
    parser.add_argument("--illegal_characters", nargs="+", default=[])
    return parser

if __name__ == "__main__":
    parser = create_parser()
    args = parser.parse_args()
    ret = main(args)
    raise SystemExit(ret)

