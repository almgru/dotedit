# dotedit
Opens the configuration file (dotfile) for a given program. 

## Usage

Open configuration file for conky:

```bash
$ dotedit c<TAB>        # <-- Tab-completion for bash, zsh & fish!
$ dotedit conky
# opens ~/.config/conky/conky.conf in $EDITOR
```

If dotedit does not know the path to the dotfile for a program, it will try to find it in `$XDG_CONFIG_HOME` or `$HOME`. It will always prompt before adding a path to avoid opening the wrong file:

```bash
$ dotedit bspwm
Add path to bspwm: ~/.config/bspwm/bspwmrc        # <-- Tab-completion works here too!
#opens ~/.config/bspwm/bspwmrc in $EDITOR
```

dotedit will, of course, save the path for next time:

```bash
$ dotedit bspwm
#opens ~/.config/bspwm/bspwmrc in $EDITOR
```

If you mistype...

```bash
$ dotedit xinit
Add path to xinit: ~/.xinitcr        # <-- Doh!
```

...you can update the path...

```bash
$ dotedit --update xinit
Update path to xinit: ~/.xinitcr
Update path to xinit: ~/.xinit
Update path to xinit: ~/.xinitrc
```

...or just remove it:

```bash
$ dotedit --remove xinit
```
