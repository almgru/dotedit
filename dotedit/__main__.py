import sys
import os
import os.path
import argparse
import subprocess
import readline

from ._path_completer import _PathCompleter
from ._path_store import _PathStore
from ._path_matcher import _PathMatcher


def main():
    parser = init_argparse()
    args = parser.parse_args()
    data_path = (os.environ.get('XDG_DATA_HOME',
                 os.environ.get('HOME') + '/.local/share') + '/dotedit')

    store = _PathStore(data_path)

    if args.list:
        for program in store.list():
            print(program)

        return 0
    elif args.remove:
        store.remove(args.remove)

        return 0
    elif args.update:
        try:
            existing = store.get(args.update)
        except LookupError:
            return 1

        path = read_path("Add path to {0}: ".format(args.update),
                         existing)
        store.update(args.update, path)

        return 0
    elif args.program != "none":
        try:
            path = store.get(args.program)
        except LookupError:
            path = read_path("Add path to {0}: ".format(args.program),
                             _PathMatcher().best_match(args.program))
            store.add(args.program, path)

        open_editor(path)

        return 0
    else:
        parser.print_usage()

        return -1


def init_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument("program", nargs="?", default="none",
                        help="program to edit dotfile of")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list programs with known paths and exit")
    parser.add_argument("-r", "--remove",
                        help="remove an entry and exit")
    parser.add_argument("-u", "--update",
                        help="update an entry and exit")

    return parser


def open_editor(path):
    subprocess.call([os.environ.get("EDITOR", "nano"), path])


def read_path(prompt, initial_buf):
    def pre_input_hook():
        readline.insert_text(initial_buf)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set match-hidden-files on")
    readline.set_completer(_PathCompleter().complete)
    path = input(prompt)
    readline.set_pre_input_hook()
    readline.set_completer()

    return path


def create_dotfile_dirs(path):
    try:
        os.makedirs(os.path.dirname(path))
    except OSError as e:
        if e.errno != os.errno.EEXIST:
            raise


if __name__ == "__main__":
    sys.exit(main())
