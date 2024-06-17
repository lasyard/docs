# Visual Studio Code

<https://code.visualstudio.com/>

Code editing. Redefined. Free. Built on open source. Runs everywhere.

## For macOS

Set key repeating on macOS:

```sh
defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false
```

Install `im-select` for vim input method switching:

```sh
curl -Ls https://raw.githubusercontent.com/daipeihust/im-select/master/install_mac.sh | sh
```

See <https://github.com/daipeihust/im-select>.

Check `im-select` installation:

```sh
which im-select
```

{.cli-output}

```sh
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

## Code Formatting

### shell

On macOS, install `shfmt`:

```sh
brew install shfmt
```

```sh
vi "${HOME}/Library/Application Support/Code/User/settings.json"
```

{.file-content}

```json
{
    "shellformat.path": "/usr/local/bin/shfmt"
}
```
