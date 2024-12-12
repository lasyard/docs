# Apache 2

<https://httpd.apache.org/>

::::{plat} macos
:vers: macOS Monterey

## Install

`apache2` is pre-installed on macOS Monterey as `httpd`.

Check the version:

```console
$ httpd -v
Server version: Apache/2.4.56 (Unix)
Server built:   Aug 17 2023 06:34:44
```

Start the server:

```sh
sudo apachectl start
```

Restart the server:

```sh
sudo apachectl -k restart
```

:::{warning}
Remember to check the config file before restart the server:

```sh
apachectl configtest
```

:::

Stop the server:

```sh
sudo apachectl stop
```

Make it start at boot:

```sh
sudo launchctl load -w /System/Library/LaunchDaemons/org.apache.httpd.plist
```

### Enable php

You need install `php` mannually for php is deprecated in macOS Monterey.

Code signing is required on new macOS versions, so a certificate authority (CA) is needed to sign the php library. See [How to create Certificate Authority for Code Signing in macOS](https://www.simplified.guide/macos/keychain-ca-code-signing-create) to create a CA.

:::{tip}
Certificates are stored in `~/Library/Application Support/Certificate Authority/`.
:::

Then sign the `php` lib:

```sh
codesign --sign 'XXXX' --force --keychain ~/Library/Keychains/login.keychain-db /usr/local/opt/php/lib/httpd/modules/libphp.so
```

Check the signature:

```console
$ codesign -dv --verbose=4 /usr/local/opt/php/lib/httpd/modules/libphp.so 2>&1 | grep Authority=
Authority=XXXX's CA
```

Add php MIME types:

```sh
sudo vi /etc/apache2/mime.types
```

:::{literalinclude} /_files/macos/etc/apache2/mime.types
:diff: /_files/macos/etc/apache2/mime.types.orig
:class: file-content
:::

Edit apache config file:

```sh
sudo vi /etc/apache2/httpd.conf
```

:::{literalinclude} /_files/macos/etc/apache2/httpd.conf
:diff: /_files/macos/etc/apache2/httpd.conf.orig
:class: file-content
:::

:::{note}
CA Name is appended to the LoadModule line for `php`.
:::

### Enable user directory access

```sh
sudo vi /etc/apache2/extra/httpd-userdir.conf
```

:::{literalinclude} /_files/macos/etc/apache2/extra/httpd-userdir.conf
:diff: /_files/macos/etc/apache2/extra/httpd-userdir.conf.orig
:class: file-content
:::

Create config file for user `xxxx`:

```sh
sudo vi /etc/apache2/users/xxxx.conf
```

:::{literalinclude} /_files/macos/etc/apache2/users/xxxx.conf
:language: apacheconf
:class: file-content
:::

Craete web root directory for user `xxxx`:

```sh
mkdir /Users/xxxx/Sites
```

Add user `_www` to `staff` group to allow apache to access the user's web root directory:

```sh
sudo dseditgroup -o edit -t user -a _www staff
dseditgroup -o read staff
```

:::{warning}
This is dangerous if you want to expose your web root directory to the public.
:::

See this URL:

```sh
open http://localhost/~xxxx/
```

::::
