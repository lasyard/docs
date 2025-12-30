# Install PHP Development Evironment

## Install

::::{tab-set}
:::{tab-item} macOS Monterey
:sync: macos

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

:::
:::{tab-item} Debian 12

```console
$ sudo apt install php
$ sudo apt install php-mysql
$ sudo apt install php-mbstring
$ sudo apt install php-xml
$ sudo apt install php-gd
$ sudo apt install php-imagick
```

:::
::::

## Configure

:::::{tab-set}
::::{tab-item} macOS Monterey
:sync: macos

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
::::
::::{tab-item} Debian 12

Use development config:

```console
$ sudo ln -snvf php.ini-development /etc/php/8.2/apache2/php.ini 
'/etc/php/8.2/apache2/php.ini' -> 'php.ini-development'
```

Set mod to access session dir:

```console
$ sudo chmod a+r /var/lib/php/sessions/
```

::::
:::::
