# Install Development Tools on CentOS

## C/C++

Install build tool set:

```sh
dnf install gcc-toolset-11
```

To use the toolset in a new shell session, run:

```sh
scl enable gcc-toolset-11 bash
```

or just do the following in the current shell:

```sh
source "/opt/rh/gcc-toolset-11/enable"
```

You can put the above command in your login scripts.

For `rpmbuild`, the tool itself and a gcc toolset plugin is needed:

```sh
dnf install rpm-build
dnf install gcc-toolset-11-annobin-plugin-gcc
```

Install other tools:

```sh
dnf install autoconf
dnf install automake
dnf install libtool
```

Install clang tools (clang-format, clang-tidy, etc.):

```sh
dnf install clang-tools-extra
```

## Go

Install Go using `dnf` (The version is quite old, os it is not recomended):

```sh
dnf install go-toolset
```

Donwload and install Go manually:

```sh
wget https://go.dev/dl/go1.22.1.linux-amd64.tar.gz
rm -rf /usr/local/go
tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz
echo "PATH=\"/usr/local/go/bin:\${PATH}\"" > /etc/profile.d/go.sh
```
