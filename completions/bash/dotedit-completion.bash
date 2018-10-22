#!/usr/bin/env bash
complete -W "-h --help -l --list -r --remove -u --update $(dotedit --list)" dotedit
