# Visual Studio Code

<https://code.visualstudio.com/>

:::{plat} macos
:vers: macOS Monterey

Set key repeating on macOS:

```sh
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```

To edit user settings directory:

```sh
vi "${HOME}/Library/Application Support/Code/User/settings.json"
```

:::

## Input method

:::{plat} macos

Install `im-select` for vim input method switching:

```sh
curl -Ls https://raw.githubusercontent.com/daipeihust/im-select/master/install_mac.sh | sh
```

See <https://github.com/daipeihust/im-select>.

Check `im-select` installation:

```console
$ which im-select
/usr/local/bin/im-select
```

Set `im-select` as the input method switching command in VSCode:

{.file-content}

```json
{
  "vim.autoSwitchInputMethod.enable": true,
  "vim.autoSwitchInputMethod.defaultIM": "com.apple.keylayout.ABC",
  "vim.autoSwitchInputMethod.obtainIMCmd": "/usr/local/bin/im-select",
  "vim.autoSwitchInputMethod.switchIMCmd": "/usr/local/bin/im-select {im}"
}
```

:::

## Code Formatting

### shell

:::{plat} macos

```sh
brew install shfmt
```

```console
$ shfmt --version
3.8.0
```

Configure VSCode to use `shfmt` for formatting shell scripts:

{.file-content}

```json
{
    "shellformat.path": "/usr/local/bin/shfmt"
}
```

:::

:::{plat} centos

```sh
wget https://github.com/patrickvane/shfmt/releases/download/master/shfmt_linux_amd64
chmod +x shfmt_linux_amd64
sudo cp shfmt_linux_amd64 /usr/local/bin/shfmt
```

```console
$ shfmt --version
(devel)
```

:::

### C

:::{plat} ubuntu

Install `clangd`:

```sh
sudo apt install clangd
```

```console
$ clangd --version
Ubuntu clangd version 14.0.0-1ubuntu1.1
Features: linux+grpc
Platform: x86_64-pc-linux-gnu
```

Install clangd plugin in VSCode, then set:

```json
{
    "clangd.path": "/usr/bin/clangd"
}

:::