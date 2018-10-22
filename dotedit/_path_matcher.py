import os
import os.path


class _PathMatcher:

    def best_match(self, program):
        home_path = os.environ.get('HOME')
        default_config_path = home_path + '/.config'
        config_path = os.environ.get('XDG_CONFIG_HOME', default_config_path)
        best_match = config_path + '/'

        matches = [f for f in os.listdir(config_path)
                   if f.casefold().startswith(program.casefold())]

        if len(matches) == 1:
            best_match += matches[0]

            if os.path.exists(best_match):
                files = os.listdir(best_match)

                if len(files) == 1:
                    best_match += '/' + files[0]
        elif len(matches) == 0:
            matches = [f for f in os.listdir(home_path)
                       if f.casefold().startswith('.')
                       and f.casefold().startswith('.' + program.casefold())]

            if len(matches) > 0:
                best_match = home_path

            if len(matches) == 1:
                best_match += '/' + matches[0]
            elif len(matches) > 1:
                best_match += '/.' + program
        else:
            best_match += program

        return best_match
