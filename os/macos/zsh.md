# zsh

`zsh` is the default shell on macOS Monterey.

Install ["Oh My Zsh"](https://ohmyz.sh/):

```console
$ sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

Check the version:

```console
$ omz version
master (69a6359)
```

Edit startup scripts `~/.zshrc`:

:::{literalinclude} /_files/macos/home/zshrc
:diff: /_files/macos/home/zshrc.orig
:::

:::{note}
The last lines are added during installation of `nvm`, see "<project:/devel/js/node.md#using-nvm>". Do not edit it mannully.
:::

Mannully update:

```console
$ omz update
```
