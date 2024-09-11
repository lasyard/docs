# shell

:::{plat} macos
:vers: macOS Monterey

Show shell version:

```sh
${SHELL} --version
```

{.cli-output}

```text
zsh 5.8.1 (x86_64-apple-darwin21.0)
```

:::

## Usage

### Date

Translate from unix timestamp to ymdhms:

```sh
date -j -f "%s" "+%Y-%m-%d %H:%M:%S" 1012586522
date -j -f "%s" "+%y%m%d_%H%M%S" 1012586522
```

Translate from ymdhms (2002.02.02 02:02:02) to unix timestamp:

```sh
date -j -f "%y%m%d%H%M%S" "+%s" 020202020202
```

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
