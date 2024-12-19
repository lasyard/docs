# gpg

<https://www.gnupg.org/>

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install gpg
```

Check the version:

:::{literalinclude} /_files/macos/console/gpg/version.txt
:language: console
:::

::::

## Usage

### Generate key

```sh
gpg --full-generate-key
```

### List keys

List public keys:

```sh
gpg -k
gpg --list-keys
```

List secret keys:

```sh
gpg -K
gpg --list-secret-keys
```

### Import key

```sh
gpg --import xxxx-key-file
```

### Verify

```sh
gpg --verify *.sig
```

### Delete key

```sh
gpg --delete-keys xxxx-key-fingerprint
```

### Key servers

```sh
gpg --keyserver hkp://pool.sks-keyservers.net --send-keys xxxx-key-fingerprint
gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys xxxx-key-fingerprint
gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys xxxx-key-fingerprint
```

### Export

```sh
gpg --export-secret-keys > secring.gpg
```

Show keys in the exported file:

```sh
gpg --show-keys secring.gpg
```

### Renew expired keys

```sh
gpg --edit-key xxxx-key-fingerprint
```

In `gpg` command line:

```sh
expire
save
quit
```
