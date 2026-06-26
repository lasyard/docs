# PyEnv

<https://github.com/pyenv/pyenv>

## Install

:::::{tab-set}
::::{tab-item} macOS
:sync: macos

Install using `brew`:

```console
$ brew install pyenv
```

Add the following code to your shell startup file (for zsh, it is `.zshrc`):

```sh
if command -v pyenv > /dev/null; then
    eval "$(pyenv init -)"
fi
```

::::
::::{tab-item} Ubuntu
:sync: ubuntu

```console
$ curl -fsSL https://pyenv.run | bash
Cloning into '/home/ubuntu/.pyenv'...
...
WARNING: seems you still have not added 'pyenv' to the load path.

# Load pyenv automatically by appending
# the following to 
# ~/.bash_profile if it exists, otherwise ~/.profile (for login shells)
# and ~/.bashrc (for interactive shells) :

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"

# Restart your shell for the changes to take effect.

# Load pyenv-virtualenv automatically by adding
# the following to ~/.bashrc:

eval "$(pyenv virtualenv-init -)"
```

Add the scripts mentioned above to `.bashrc` (Generally, `.profile` would call `.bashrc` on Ubuntu).

::::
:::::

Show the version:

```console
$ pyenv --version 
pyenv 2.4.11
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

> [!TIP]
> For PyEnv install python by building from sources, so some other dependencies may have to be installed first. See <project:install.md>.
>
> List all installable versions:
>
> ```console
> $ pyenv install --list
> ```

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
