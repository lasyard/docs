# gpg

<https://www.gnupg.org/>

GnuPG is a complete and free implementation of the OpenPGP standard as defined by RFC4880 (also known as PGP). GnuPG allows you to encrypt and sign your data and communications; it features a versatile key management system, along with access modules for all kinds of public key directories. GnuPG, also known as GPG, is a command line tool with features for easy integration with other applications. A wealth of frontend applications and libraries are available. GnuPG also provides support for S/MIME and Secure Shell (ssh).

## Install

::::{plat} macos
:vers: macOS Monterey

```sh
brew install gpg
```

```sh
gpg --version
```

:::{literalinclude} /_files/macos/output/gpg/version.txt
:language: text
:class: cli-output
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
