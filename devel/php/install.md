# Install PHP Development Evironment

## Install on macOS Monterey

```console
$ brew install php
```

Check the version:

```console
$ php -v
PHP 8.3.11 (cli) (built: Aug 30 2024 16:34:18) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.3.11, Copyright (c) Zend Technologies
```

## Configure

See where to find `ini` configuration:

```console
$ php --ini
Configuration File (php.ini) Path: /usr/local/etc/php/8.3
Loaded Configuration File:         /usr/local/etc/php/8.3/php.ini
Scan for additional .ini files in: /usr/local/etc/php/8.3/conf.d
Additional .ini files parsed:      /usr/local/etc/php/8.3/conf.d/ext-opcache.ini
```

For macOS Monterey, you need to disable loading opcache, for there is no way to set code sign for it. To do this, edit file `/usr/local/etc/php/8.3/conf.d/opcache.ini`:

:::{literalinclude} /_files/macos/etc/php/8.3/conf.d/ext-opcache.ini
:diff: /_files/macos/etc/php/8.3/conf.d/ext-opcache.ini.orig
:::
