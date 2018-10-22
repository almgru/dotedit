import os
import os.path
import readline


class _PathCompleter:

    def complete(self, text, state):
        if state == 0:
            dir_ = os.path.dirname(readline.get_line_buffer())

            if os.path.exists(dir_):
                os.chdir(dir_)

            if dir_ != "":
                self.matches = [
                    f
                    for f in os.listdir(os.curdir)
                    if f.startswith(text)]

        try:
            result = self.matches[state]
        except IndexError:
            result = None

        if len(self.matches) == 1:
            path = os.curdir + "/" + result
            if os.path.isdir(path):
                result += '/'

        return result
