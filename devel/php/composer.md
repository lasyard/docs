# composer

<https://getcomposer.org/>

## Install

::::{plat} macos

```sh
brew install composer
```

:::{tip}
PHP is also installed as a dependency.
:::

Check the version:

:::{literalinclude} /_files/macos/console/composer/version.txt
:language: console
:::

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
