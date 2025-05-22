# gpg

<https://www.gnupg.org/>

## Install

::::{tabs}
:::{tab} macOS Monterey
Install using `brew`:

```console
$ brew install gpg
```

Check the version:

```console
$ gpg --version
gpg (GnuPG) 2.4.5
libgcrypt 1.10.3
Copyright (C) 2024 g10 Code GmbH
License GNU GPL-3.0-or-later <https://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Home: /Users/xxxx/.gnupg
支持的算法：
公钥： RSA, ELG, DSA, ECDH, ECDSA, EDDSA
密文： IDEA, 3DES, CAST5, BLOWFISH, AES, AES192, AES256, TWOFISH,
    CAMELLIA128, CAMELLIA192, CAMELLIA256
散列： SHA1, RIPEMD160, SHA256, SHA384, SHA512, SHA224
压缩：  不压缩, ZIP, ZLIB, BZIP2
```

:::
::::

## Usage

### Generate key

```console
$ gpg --full-generate-key
```

### List keys

List public keys:

```console
$ gpg -k
$ gpg --list-keys
```

List secret keys:

```console
$ gpg -K
$ gpg --list-secret-keys
```

### Import key

```console
$ gpg --import xxxx-key-file
```

### Verify

```console
$ gpg --verify *.sig
```

### Delete key

```console
$ gpg --delete-keys xxxx-key-fingerprint
```

### Key servers

```console
$ gpg --keyserver hkp://pool.sks-keyservers.net --send-keys xxxx-key-fingerprint
$ gpg --keyserver hkp://pool.sks-keyservers.net --recv-keys xxxx-key-fingerprint
$ gpg --keyserver hkp://keyserver.ubuntu.com --recv-keys xxxx-key-fingerprint
```

### Export

```console
$ gpg --export-secret-keys > secring.gpg
```

Show keys in the exported file:

```console
$ gpg --show-keys secring.gpg
```

### Renew expired keys

```console
$ gpg --edit-key xxxx-key-fingerprint
```

In `gpg` command line:

```sh
expire
save
quit
```
