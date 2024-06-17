# Install PHP

## macOS

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

```sh
codesign --sign 'XXXX' --force --keychain ~/Library/Keychains/login.keychain-db /usr/local/opt/php/lib/php/20230831/opcache.so
```
