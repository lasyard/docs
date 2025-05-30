# shell

## Show version

::::{tab-set}
:::{tab-item} macOS Monterey

```console
$ ${SHELL} --version
zsh 5.8.1 (x86_64-apple-darwin21.0)
```

:::
::::

## Date

::::{tab-set}
:::{tab-item} macOS Monterey

Translate from unix timestamp to `ymdhms`:

```console
$ date -j -f "%s" "+%Y-%m-%d %H:%M:%S" 1737000000
2025-01-16 12:00:00
```

Translate from `ymdhms` to unix timestamp:

```console
$ date -j -f "%Y-%m-%d %H:%M:%S" "+%s" "2025-01-16 12:00:00"
1737000000
```

:::
::::

## Remove executable flags recursively

```console
$ sudo chmod -R -x photo
$ chmod -R +X photo
```

## Find empty directories

Find empty directories:

```console
$ find . -type d -empty
```

Also delete them:

```console
$ find . -type d -empty -delete
```
