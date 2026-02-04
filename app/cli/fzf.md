# fzf

<https://github.com/junegunn/fzf>

## Install

By package manager:

::::{tab-set}
:::{tab-item} macOS Monterey
:sync: macos

```console
$ brew install fzf
...
==> Pouring fzf--0.55.0.monterey.bottle.tar.gz
==> Caveats
To set up shell integration, add this to your shell configuration file:
  # bash
  eval "$(fzf --bash)"

  # zsh
  source <(fzf --zsh)

  # fish
  fzf --fish | source
```

:::
::::

Use binary release:

```console
$ curl -LO https://github.com/junegunn/fzf/releases/download/v0.67.0/fzf-0.67.0-darwin_amd64.tar.gz
$ tar -C /usr/local/bin -xzf fzf-0.67.0-darwin_amd64.tar.gz
```
