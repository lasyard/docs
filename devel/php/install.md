# Install PHP

::::{plat} macos
:vers: macOS Monterey

```sh
brew install php
```

```sh
php -v
```

:::{literalinclude} /_files/macos/output/php/v.txt
:language: text
:class: cli-output
:::

## Configure

See where to find `ini` configuration:

```sh
php --ini
```

:::{literalinclude} /_files/macos/output/php/ini.txt
:language: text
:class: cli-output
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
