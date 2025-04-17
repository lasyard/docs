# git

<https://git-scm.com/>

## Install

::::{tabs}
:::{tab} CentOS

```console
$ sudo dnf install git
```

```console
$ git --version
git version 2.27.0
```

:::
:::{tab} macOS

`git` is pre-installed on macOS.

```console
$ git --version
git version 2.37.1 (Apple Git-137.1)
```

::::

## Usage

### Show config

```console
$ git config -l
```

### Set config

```console
$ git config --global init.defaultBranch main
$ git config --global submodule.recurse true
$ git config --global push.recurseSubmodules check
$ git config --global url.git@github.com:.insteadOf https://github.com/
$ git config --global url.https://github.com/.insteadOf git@github.com:
$ git config --global pull.ff only
```

If you want to show unicode characters in filename:

```console
$ git config core.quotePath false
```

### Unset config

```console
$ git config --unset pull.ff
```

### See last commit

```console
$ git log -p -1
$ git show
```

Briefly, only show names and status:

```console
$ git show --name-status
```

### Stash with untracked files

```console
$ git stash --include-untracked
$ git stash -u
```

### Clean

```console
$ git clean -dxf
```
