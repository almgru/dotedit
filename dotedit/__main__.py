import sys
import os
import os.path
import argparse
import readline

from pkg_resources import resource_stream
from subprocess import call
from shutil import copy

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
    elif args.completions:
        print_comp_script(args.completions)
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

        open_editor(path, not args.no_hooks)
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
    parser.add_argument("--completions", metavar="SHELL",
                        help=("output completion script for SHELL. " +
                              "(bash, zsh & fish currently supported)"))
    parser.add_argument("-n", "--no-hooks", action="store_true",
                        help="Do not run pre or post edit hooks")

    return parser


def open_editor(path, run_hooks):
    if run_hooks:
        run_hook("pre-edit")

    call([os.environ.get("EDITOR", "nano"), path])

    if run_hooks:
        run_hook("post-edit")


def run_hook(name):
    hook = get_config_directory() + "/hooks/" + name

    if os.path.exists(hook) and os.access(hook, os.X_OK):
        call([hook])


def get_config_directory():
    home = os.environ.get("HOME")
    config_dir = (os.environ.get("XDG_CONFIG_HOME", home + "/.config") +
                  "/dotedit")

    return config_dir


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


def print_comp_script(shell):
    home = os.environ.get('HOME')
    config_home = os.environ.get('XDG_CONFIG_HOME')
    res_name = "completions/"

    if shell == 'bash':
        res_name += "bash/dotedit-completion.bash"
    elif shell == 'zsh':
        res_name += "zsh/_dotedit"
    elif shell == 'fish':
        res_name += "fish/dotedit.fish"
    else:
        raise ValueError("Completions not supported for this shell")

    print(resource_stream(__name__, res_name).read().decode())


if __name__ == "__main__":
    sys.exit(main())
