import sys
import os
import os.path
import argparse
import subprocess
import readline

from ._path_completer import _PathCompleter
from ._path_store import _PathStore
from . import _path_matcher


def main():
    parser = init_argparse()
    args = parser.parse_args()
    data_path = (os.environ.get('XDG_DATA_HOME',
                 os.environ.get('HOME') + '/.local/share') + '/dotedit')

    store = _PathStore(data_path)

    if args.list:
        [print(program) for program in store.list()]
    elif args.remove:
        store.remove(args.remove)
    elif args.update:
        try:
            existing = store.get(args.update)
        except LookupError:
            return 1

        path = read_path("Add path to {0}: ".format(args.update), existing)
        store.update(args.update, path)
    elif args.program != "none":
        try:
            path = store.get(args.program)
        except LookupError:
            path = read_path("Add path to {0}: ".format(args.program),
                             _path_matcher.best_match(args.program))
            store.add(args.program, path)

        open_editor(path)
    else:
        parser.print_usage()

        return 1

    return 0


def init_argparse():
    parser = argparse.ArgumentParser()

    parser.add_argument("program", nargs="?", default="none",
                        help="program to edit dotfile of")
    parser.add_argument("-l", "--list", action="store_true",
                        help="list programs with known paths and exit")
    parser.add_argument("-r", "--remove", metavar='PROGRAM',
                        help="remove PROGRAM path and exit")
    parser.add_argument("-u", "--update", metavar='PROGRAM',
                        help="update PROGRAM path and exit")

    return parser


def open_editor(path):
    subprocess.call([os.environ.get("EDITOR", "nano"), path])


def read_path(prompt, initial_text):
    def pre_input_hook():
        readline.insert_text(initial_text)
        readline.redisplay()

    readline.set_pre_input_hook(pre_input_hook)
    readline.parse_and_bind("tab: complete")
    readline.parse_and_bind("set match-hidden-files on")
    readline.set_completer(_PathCompleter().complete)
    try:
        path = input(prompt)
    except (EOFError, KeyboardInterrupt) as e:
        sys.exit(1)
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
