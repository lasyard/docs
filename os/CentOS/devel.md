# Install Development Tools on CentOS

## C/C++

Install build tool set:

```sh
dnf install gcc-toolset-11
```

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
