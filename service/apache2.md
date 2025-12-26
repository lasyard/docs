# Apache 2

<https://httpd.apache.org/>

## Install

::::{tab-set}
:::{tab-item} macOS Monterey
:sync: macos
`apache2` is pre-installed on macOS Monterey as `httpd`.

Check the version:

```console
$ httpd -v
Server version: Apache/2.4.56 (Unix)
Server built:   Aug 17 2023 06:34:44
```

Start/stop the server:

```console
$ sudo apachectl start
$ sudo apachectl stop
```

Restart the server:

```console
$ sudo apachectl -k restart
```

Check the config file:

```console
$ apachectl configtest
```

Make it start at boot:

```console
$ sudo launchctl load -w /System/Library/LaunchDaemons/org.apache.httpd.plist
```

:::
:::{tab-item} Debian 12
:sync: debian

```console
$ sudo apt install apache2
```

```console
$ sudo apache2 -v
Server version: Apache/2.4.65 (Debian)
Server built:   2025-07-29T20:18:46
```

```console
$ systemctl status apache2
● apache2.service - The Apache HTTP Server
     Loaded: loaded (/lib/systemd/system/apache2.service; enabled; preset: enabled)
     Active: active (running) since Tue 2025-12-23 03:42:21 CST; 31s ago
       Docs: https://httpd.apache.org/docs/2.4/
   Main PID: 1500 (apache2)
      Tasks: 55 (limit: 2236)
     Memory: 11.1M
        CPU: 135ms
     CGroup: /system.slice/apache2.service
             ├─1500 /usr/sbin/apache2 -k start
             ├─1501 /usr/sbin/apache2 -k start
             └─1502 /usr/sbin/apache2 -k start
```

Enable modules:

```console
$ sudo a2enmod rewrite
Enabling module rewrite.
To activate the new configuration, you need to run:
  systemctl restart apache2
```

:::
::::

## Enable php

:::::{tab-set}
::::{tab-item} macOS Monetery
:sync: macos
You need install `php` mannually for php is deprecated in macOS Monterey.

Code signing is required on new macOS versions, so a certificate authority (CA) is needed to sign the php library. See [How to create Certificate Authority for Code Signing in macOS](https://www.simplified.guide/macos/keychain-ca-code-signing-create) to create a CA.

:::{tip}
Certificates are stored in `~/Library/Application Support/Certificate Authority/`.
:::

Then sign the `php` lib:

```console
$ codesign --sign 'XXXX' --force --keychain ~/Library/Keychains/login.keychain-db /usr/local/opt/php/lib/httpd/modules/libphp.so
```

Check the signature:

```console
$ codesign -dv --verbose=4 /usr/local/opt/php/lib/httpd/modules/libphp.so 2>&1 | grep Authority=
Authority=XXXX's CA
```

Edit file `/etc/apache2/mime.types` to add php MIME types:

:::{literalinclude} /_files/macos/etc/apache2/mime.types
:diff: /_files/macos/etc/apache2/mime.types.orig
:::

Edit apache config file `/etc/apache2/httpd.conf`:

:::{literalinclude} /_files/macos/etc/apache2/httpd.conf
:diff: /_files/macos/etc/apache2/httpd.conf.orig
:::

:::{note}
CA Name is appended to the LoadModule line for `php`.
:::
::::
::::{tab-item} Debian 12
:sync: debian

See <project:/devel/php/install.md>.

::::
:::::

### Enable user directory access

:::::{tab-set}
::::{tab-item} macOS Monterey
:sync: macos
Edit apache config file `/etc/apache2/extra/httpd-userdir.conf`:

:::{literalinclude} /_files/macos/etc/apache2/extra/httpd-userdir.conf
:diff: /_files/macos/etc/apache2/extra/httpd-userdir.conf.orig
:::

Create config file `/etc/apache2/users/xxxx.conf` for user `xxxx`:

:::{literalinclude} /_files/macos/etc/apache2/users/xxxx.conf
:language: apacheconf
:::

Create web root directory for user `xxxx`:

```console
$ mkdir /Users/xxxx/Sites
```

Add user `_www` to `staff` group to allow apache to access the user's web root directory:

```console
$ sudo dseditgroup -o edit -t user -a _www staff
$ dseditgroup -o read staff
```

:::{warning}
This is dangerous if you want to expose your web root directory to the public.
:::

See this URL:

```console
open http://localhost/~xxxx/
```

::::
:::::
