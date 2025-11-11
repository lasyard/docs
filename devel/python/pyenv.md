# PyEnv

<https://pyenv.net/>

## Install

::::{tab-set}
:::{tab-item} macOS Monterey

Install using `brew`:

```console
$ brew install pyenv
```

Show the version:

```console
$ pyenv --version 
pyenv 2.4.11
```

:::
::::

Add the following code to your shell startup file (for zsh, it is `.zshrc`):

```sh
if which pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi
```

## Usage

Install a new version:

```console
$ pyenv install 3.12.5
python-build: use openssl@3 from homebrew
python-build: use readline from homebrew
Downloading Python-3.12.5.tar.xz...
-> https://www.python.org/ftp/python/3.12.5/Python-3.12.5.tar.xz
Installing Python-3.12.5...
python-build: use tcl-tk from homebrew
python-build: use readline from homebrew
Installed Python-3.12.5 to /Users/xxxx/.pyenv/versions/3.12.5
```

Show all vresions:

```console
$ pyenv versions
* system (set by /Users/xxxx/.pyenv/version)
  3.12.5
```

Set version globally:

```console
$ pyenv global 3.12.5
$ pyenv versions
  system
* 3.12.5 (set by /Users/xxxx/.pyenv/version)
```

Note the "set by" things.

Set version in current directory:

```console
$ pyenv local 3.12.5
$ pyenv versions
  system
* 3.12.5 (set by /Users/xxxx/.python-version)

Set version in current shell:

```console
$ pyenv shell 3.12.5
$ pyenv versions
  system
* 3.12.5 (set by PYENV_VERSION environment variable)
```

The decision of effective version is made by the importantce sequence: shell > local > global.
