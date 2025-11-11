# Homebrew

<https://brew.sh/>

## Install

```console
$ curl -LO https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh
$ chmod +x install.sh
$ ./install.sh
==> Checking for `sudo` access (which may request your password)...
Password:
==> You are using macOS 12.7.
==> We (and Apple) do not provide support for this old version.
This installation may not succeed.
After installation, you will encounter build failures with some formulae.
Please create pull requests instead of asking for help on Homebrew's GitHub,
Twitter or any other official channels. You are responsible for resolving any
issues you experience while you are running this old version.

==> This script will install:
/usr/local/bin/brew
/usr/local/share/doc/homebrew
/usr/local/share/man/man1/brew.1
/usr/local/share/zsh/site-functions/_brew
/usr/local/etc/bash_completion.d/brew
/usr/local/Homebrew
==> The following new directories will be created:
/usr/local/var/homebrew/linked
/usr/local/Cellar
/usr/local/Caskroom
/usr/local/Frameworks
==> HOMEBREW_NO_INSTALL_FROM_API is set.
Homebrew/homebrew-core will be tapped during this install run.

Press RETURN/ENTER to continue or any other key to abort:
==> /usr/bin/sudo /bin/mkdir -p /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /bin/chmod ug=rwx /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /usr/sbin/chown xxxx /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /usr/bin/chgrp admin /usr/local/var/homebrew/linked /usr/local/Cellar /usr/local/Caskroom /usr/local/Frameworks
==> /usr/bin/sudo /bin/mkdir -p /usr/local/Homebrew
==> /usr/bin/sudo /usr/sbin/chown -R xxxx:admin /usr/local/Homebrew
==> Downloading and installing Homebrew...
...
==> Installation successful!

==> Homebrew has enabled anonymous aggregate formulae and cask analytics.
Read the analytics documentation (and how to opt-out) here:
  https://docs.brew.sh/Analytics
No analytics data has been sent yet (nor will any be during this install run).

==> Homebrew is run entirely by unpaid volunteers. Please consider donating:
  https://github.com/Homebrew/brew#donations

==> Next steps:
- Run these commands in your terminal to add Homebrew to your PATH:
    echo >> /Users/xxxx/.zprofile
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> /Users/xxxx/.zprofile
    eval "$(/usr/local/bin/brew shellenv)"
- Run brew help to get started
- Further documentation:
    https://docs.brew.sh
```

## Usage

List all packages:

```console
$ brew list
```

List packages installed on request:

```console
$ brew list --installed-on-request 
```

Upgrade all packages:

```console
$ brew upgrade
```

Cleanup cache:

```console
$ brew cleanup -s
```

Pin a package:

```console
$ brew pin openssl@3
```

List pinned packages:

```console
$ brew list --pinned
```

Sometimes installed Kegs are not linked out from Cellar (maybe for the targets are already there installed by other tools), you can link them mannually by:

```console
$ brew link python@3.12
Linking /usr/local/Cellar/python@3.12/3.12.5... 21 symlinks created.
```

## TUNA mirror

Set the environments:

```sh
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
export HOMEBREW_PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
```

Set the remote URL of the repos:

```console
$ git -C "$(brew --repo)" remote set-url origin "${HOMEBREW_BREW_GIT_REMOTE}"
$ git -C "$(brew --repo homebrew/core)" remote set-url origin "${HOMEBREW_CORE_GIT_REMOTE}"
```

## macOS 12 problem

Support for macOS 12 has been removed. If you want to uninstall Homebrew:

```console
$ brew uninstall --force $(brew list)
$ brew untap $(brew tap)
$ brew cleanup -s
$ rm /usr/local/bin/brew
$ sudo rmdir /usr/local/{Caskroom,Cellar,Frameworks}
$ sudo rm -rf /usr/local/Homebrew
```

Or freeze Homebrew version:

```console
$ git -C "$(brew --repo)" checkout -b macOS-monterey-freeze 9042eb9
$ git -C "$(brew --repo homebrew/core)" checkout -b macOS-monterey-freeze da66cc3
```

Set these environments to disable auto updating and installing from API:

```sh
export HOMEBREW_NO_AUTO_UPDATE=1
export HOMEBREW_NO_INSTALL_FROM_API=1
```
