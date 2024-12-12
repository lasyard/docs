# Install PHP

::::{plat} macos
:vers: macOS Monterey

```sh
brew install php
```

Check the version:

:::{literalinclude} /_files/macos/console/php/v.txt
:language: console
:::

## Configure

See where to find `ini` configuration:

:::{literalinclude} /_files/macos/console/php/ini.txt
:language: console
:::

Disable opcache (for unsigned libs cannot be loaded on newer macOS):

```sh
vi /usr/local/etc/php/8.3/conf.d/opcache.ini
```

:::{literalinclude} /_files/macos/etc/php/8.3/conf.d/ext-opcache.ini
:diff: /_files/macos/etc/php/8.3/conf.d/ext-opcache.ini.orig
:class: file-content
:::

::::
