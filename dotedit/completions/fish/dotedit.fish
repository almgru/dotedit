complete --exclusive --command dotedit --long-option completions \
         --arguments "bash zsh fish" \
         --description "output completion script for SHELL. \
                        (bash, zsh & fish currently supported)"

complete --no-files --command dotedit --short-option h --long-option help \
         --description "show help and exit"

complete --no-files --command dotedit --short-option l --long-option list \
         --description "list programs with known paths and exit"

complete --no-files --command dotedit --short-option n --long-option no-hooks \
         --description "Do not run pre or post edit hooks"

complete --exclusive --command dotedit --short-option r --long-option remove \
         --arguments '(dotedit --list)' \
         --description "remove PROGRAM path and exit"

complete --exclusive --command dotedit --short-option u --long-option update \
         --arguments '(dotedit --list)' \
         --description "update PROGRAM path and exit"

complete --no-files --command dotedit --arguments '(dotedit --list)' \
         --description "program to edit dotfile of"

