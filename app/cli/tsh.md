# tsh

<https://goteleport.com/docs/connect-your-client/tsh/>

## Install

Find the server version:

:::{literalinclude} /_files/macos/console/curl/teleport_server_version.txt
:language: console
:::

::::{plat} macos
:vers: macOS Monterey

Download the package:

```sh
curl -O https://cdn.teleport.dev/tsh-16.1.8.pkg
```

::::

Then install it.

## Usage

List `tsh` profiles:

```sh
tsh status
```

Login:

```sh
tsh login --user=xxxx --proxy=https://server.teleport.xxxx
```

Ssh login:

```sh
tsh ssh xxxx@node-xxxx
```

Check status in the node you logged in:

```sh
teleport status
```
