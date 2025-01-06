# git

<https://git-scm.com/>

## Install

:::{plat} centos
:vers: CentOS 8.5

```sh
sudo dnf install git
```

```console
$ git --version
git version 2.27.0
```

:::

:::{plat} macos
:vers: macOS Monterey

`git` is pre-installed on macOS.

```console
git --version
git version 2.37.1 (Apple Git-137.1)
```

:::

## Usage

### Show config

```sh
git config -l
```

### Set config

```sh
git config --global init.defaultBranch main
git config --global submodule.recurse true
git config --global push.recurseSubmodules check
git config --global url.git@github.com:.insteadOf https://github.com/
git config --global url.https://github.com/.insteadOf git@github.com:
git config --global pull.ff only
```

If you want to show unicode characters in filename:

```sh
git config core.quotePath false
```

### Unset config

```sh
git config --unset pull.ff
```

### See last commit

```sh
git log -p -1
git show
```

```sh
git show --name-status
```

### Stash with untracked files

```sh
git stash --include-untracked
git stash -u
```

### Clean

```sh
git clean -dxf
```
