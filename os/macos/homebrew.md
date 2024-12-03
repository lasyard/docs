# Homebrew

<https://brew.sh/>

The Missing Package Manager for macOS (or Linux).

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
