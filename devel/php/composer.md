# composer

<https://getcomposer.org/>

A Dependency Manager for PHP.

## Install

### macOS

:CPU: x86_64 * 2
:OS: macOS Monterey

```sh
brew install composer
```

:::{tip}
PHP is also installed as a dependency.
:::

```sh
composer --version
```

{.cli-output}

```text
Composer version 2.7.6 2024-05-04 23:03:15
PHP version 8.3.7 (/usr/local/Cellar/php/8.3.7/bin/php)
Run the "diagnose" command to get more detailed diagnostics output.
```

## Usage

Create a basic `composer.json` file in current directory:

```sh
composer init
```

Install:

```sh
composer install
```

This command installs the project dependencies from the `composer.lock` file if present, or falls back on the `composer.json` file.

Test:

```sh
composer test
```
