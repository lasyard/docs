# git

<https://git-scm.com/>

Git is a free and open source distributed version control system designed to handle everything from small to very large projects with speed and efficiency.

## Usage

### Show version

:::{plat} macos

```sh
git --version
```

{.cli-output}

```text
git version 2.37.1 (Apple Git-137.1)
```

:::

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
