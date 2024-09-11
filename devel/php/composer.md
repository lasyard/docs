# composer

<https://getcomposer.org/>

A Dependency Manager for PHP.

## Install

::::{plat} macos

```sh
brew install composer
```

:::{tip}
PHP is also installed as a dependency.
:::

```sh
composer --version
```

:::{literalinclude} /_files/macos/output/composer/version.txt
:language: text
:class: cli-output
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
