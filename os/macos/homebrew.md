# Homebrew

<https://brew.sh/>

## Install

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

## Usage

List all packages:

```sh
brew list
```

List packages installed on request:

```sh
brew list --installed-on-request 
```

Upgrade all packages:

```sh
brew upgrade
```

Cleanup cache:

```sh
brew cleanup -s
```

Pin a package:

```sh
brew pin openssl@3
```

List pinned packages:

```sh
brew list --pinned
```

## TUNA mirror

```sh
export HOMEBREW_API_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles/api"
export HOMEBREW_BOTTLE_DOMAIN="https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles"
export HOMEBREW_BREW_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git"
export HOMEBREW_CORE_GIT_REMOTE="https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git"
export HOMEBREW_PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"
```

```sh
git -C "$(brew --repo)" remote set-url origin "${HOMEBREW_BREW_GIT_REMOTE}"
git -C "$(brew --repo homebrew/core)" remote set-url origin "${HOMEBREW_CORE_GIT_REMOTE}"
```

## macOS 12 problem

Support for macOS 12 has been removed. If you want to uninstall Homebrew:

```sh
brew uninstall --force $(brew list)
brew untap $(brew tap)
brew cleanup -s
rm /usr/local/bin/brew
sudo rmdir /usr/local/{Caskroom,Cellar,Frameworks,Homebrew}
```

Or freeze Homebrew version:

```sh
git -C "$(brew --repo)" checkout -b macOS-monterey-freeze 9042eb9
git -C "$(brew --repo homebrew/core)" checkout -b macOS-monterey-freeze da66cc3
```

```sh
export HOMEBREW_NO_AUTO_UPDATE=1
export HOMEBREW_NO_INSTALL_FROM_API=1
```
