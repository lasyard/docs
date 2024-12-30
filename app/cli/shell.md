# shell

:::{plat} macos
:vers: macOS Monterey

Show shell version:

```console
$ ${SHELL} --version
zsh 5.8.1 (x86_64-apple-darwin21.0)
```

:::

## Usage

### Date

:::{plat} macos
:vers: macOS Monterey

Translate from unix timestamp to ymdhms:

```console
$ date -j -f "%s" "+%Y-%m-%d %H:%M:%S" 1735660800
2025-01-01 00:00:00
```

Translate from ymdhms to unix timestamp:

```console
$ date -j -f "%Y-%m-%d %H:%M:%S" "+%s" "2025-01-01 00:00:00"
1735660800
```

:::

### Remove executable flags recursively

```sh
sudo chmod -R -x photo
chmod -R +X photo
```

### Find empty directories (and delete them)

```sh
find . -type d -empty
find . -type d -empty -delete
```
