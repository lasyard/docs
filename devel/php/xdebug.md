# Xdebug

<https://xdebug.org/>

## Install

::::{tab-set}
:::{tab-item} Debian 12
:sync: debian

```console
$ sudo apt install php-xdebug
```

Show php version info to see Xdebug is enabled:

```console
$ php -v
PHP 8.2.29 (cli) (built: Jul  3 2025 16:16:05) (NTS)
Copyright (c) The PHP Group
Zend Engine v4.2.29, Copyright (c) Zend Technologies
    with Zend OPcache v8.2.29, Copyright (c), by Zend Technologies
    with Xdebug v3.2.0, Copyright (c) 2002-2022, by Derick Rethans
```

:::
::::

## Configure

:::::{tab-set}
::::{tab-item} Debian 12
:sync: debian

Edit file `/etc/php/8.2/apache2/conf.d/20-xdebug.ini`:

:::{literalinclude} /_files/debian/etc/php/8.2/apache2/conf.d/20-xdebug.ini
:diff: /_files/debian/etc/php/8.2/apache2/conf.d/20-xdebug.ini.orig
:::

Make sure the log file can be accessed by the apache server:

```console
$ sudo touch /var/log/xdebug.log
$ sudo chown www-data:www-data /var/log/xdebug.log
```

In vscode `launch.json`:

```json
{
    "name": "Listen for Xdebug",
    "type": "php",
    "request": "launch",
    "port": 9003,
    "pathMappings": {
        "/mnt/hgfs": "/Users/xxxx"
    }
}
```

::::
:::::
