# composer

<https://getcomposer.org/>

## Install on macOS Monterey

```console
$ brew install composer
```

:::{tip}
PHP is also installed as a dependency.
:::

Check the version:

```console
$ composer --version
Composer version 2.7.9 2024-09-04 14:43:28
PHP version 8.3.11 (/usr/local/Cellar/php/8.3.11/bin/php)
Run the "diagnose" command to get more detailed diagnostics output.
```

## Usage

Create a basic `composer.json` file in current directory by:

```console
$ composer init
```

Install components:

```console
$ composer install
```

This command installs the project dependencies from the `composer.lock` file if present, or falls back on the `composer.json` file.

Test:

```console
$ composer test
```
