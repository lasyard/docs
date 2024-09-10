# zsh

`zsh` is the default shell on macOS Monterey.

Install ["Oh My Zsh"](https://ohmyz.sh/):

```sh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

```sh
omz version
```

{.cli-ouput}

```text
master (373a1fd)
```

Edit startup scripts:

```sh
vi ~/.zshrc
```

:::{literalinclude} /_files/macos/home/zshrc
:diff: /_files/macos/home/zshrc.orig
:class: file-content
:::

Mannully update:

```sh
omz update
```
