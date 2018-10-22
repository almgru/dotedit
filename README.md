# dotedit
Simple script that opens the configuration file for a given program.

## Usage

Open configuration file for conky:

```bash
$ dotedit conky
# opens ~/.config/conky/conky.conf in $EDITOR
```

dotedit is very stupid and does not make any assumptions about where you store your config files. If it does not know, it asks, and saves your answer for next time:

```bash
$ dotedit bspwm
Add path to bspwm: /home/USER/.config/bspwm/bspwmrc
#opens ~/.config/bspwm/bspwmrc in $EDITOR
...
$ dotedit bspwm
#opens ~/.config/bspwm/bspwmrc in $EDITOR
```
