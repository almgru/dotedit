# dotedit
Opens the configuration file (dotfile) for a given program. 

#### Contents
1. [Usage](#usage)
2. [Install](#install)
    * [Bash](#bash)
    * [Zsh](#zsh)
    * [fish](#fish)

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

## Hooks
You can add pre and post hooks by creating the files
`$XDG_CONFIG_HOME/dotedit/hooks/pre-edit` and 
`$XDG_CONFIG_HOME/dotedit/hooks/postedit` and making them executable.

For example to automatically commit and push changes to dotfiles in a git
directory you can create post edit hook with the following content:

```bash
#!/bin/sh

cd $HOME/git/dotfiles/
git add -A . && git commit -m 'update' && git pull --rebase && git push
```

## Install

```bash
$ pip3 install --user dotedit
```

### Completions
To enable completions, the completion scripts need to be installed manually. 

#### Bash
```bash
$ dotedit --completions bash > ~/.local/share/bash-completion/completions/dotedit
```

#### Zsh

```zsh
$ dotedit --completions zsh > ~/.zfunc/_dotedit
```

#### fish

```fish
$ dotedit --completions fish > ~/.config/fish/completions/dotedit.fish
```

Finally, restart your shell session or source the completion script to enable completions.
